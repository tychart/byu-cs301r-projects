# Before running this script:
# pip install gradio openai

import argparse
import asyncio
import json
import random
import re
from pathlib import Path
import html

import gradio as gr
from openai import AsyncOpenAI
from openai.types.shared_params.reasoning import Reasoning
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from tools import ToolBox
from usage import print_usage, format_usage_markdown
from weather import get_weather

our_tools = ToolBox()

our_tools.tool(get_weather)

from dotenv import load_dotenv
load_dotenv()

BASE = "https://www.churchofjesuschrist.org"


@our_tools.tool
def get_random_number(lower: int, upper: int) -> int:
    """Get a random number"""
    return random.randint(lower, upper)

@our_tools.tool
def get_website_from_url(url: str) -> str:
    """Get the python requests response from a website from the URL given"""
    return requests.get(url).text

@our_tools.tool
def get_gc_speaker_name_index() -> list[dict]:
    """
    Return a list of speakers from the GC speakers index as a JSON-serializable list.
    Each item: {"name": "<display name>", "url_name": "<url slug>", "url": "<full url>"}
    """
    url = "https://www.churchofjesuschrist.org/study/general-conference/speakers?lang=eng"
    resp_text = requests.get(url, timeout=15).text
    soup = BeautifulSoup(resp_text, "html.parser")

    pattern = re.compile(r"^/study/general-conference/speakers/([^/?]+)")
    seen = set()
    results = []

    for a in soup.find_all("a", href=True):
        m = pattern.match(a["href"])
        if not m:
            continue
        url_name = m.group(1)  # e.g. "d-todd-christofferson"
        # Try to get a reasonable display name: text in the anchor or an inner <h4> etc.
        name = a.get_text(separator=" ", strip=True)
        # If anchor text contains things other than the name (e.g., empty), try to find a child title
        if not name:
            h4 = a.find("h4")
            if h4:
                name = h4.get_text(separator=" ", strip=True)
        if not name:
            # fallback to the slug (replace hyphens with spaces, title-case)
            name = url_name.replace("-", " ").title()

        # Avoid duplicates
        if url_name in seen:
            continue
        seen.add(url_name)

        full = urljoin(BASE, a["href"])
        # normalize: strip query string / fragment
        parsed = urlparse(full)
        normalized = parsed._replace(query="", fragment="").geturl()

        results.append({
            "name": name,
            "url_name": url_name,
            "url": normalized
        })

    return results

@our_tools.tool
def get_gc_speaker_talk_index(url_name: str) -> str:
    page_url = f"{BASE}/study/general-conference/speakers/{url_name}?lang=eng"
    headers = {"User-Agent": "gc-speaker-index-parser/1.0"}
    resp = requests.get(page_url, headers=headers, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    results = []

    # helper to make a safe debug print
    def safe_print(*parts):
        try:
            print(*parts)
        except UnicodeEncodeError:
            # fall back to a replace-encoded representation
            safe_parts = []
            for p in parts:
                s = str(p)
                s = s.encode("utf-8", errors="replace").decode("utf-8")
                safe_parts.append(s)
            print(*safe_parts)

    # iterate year headings and then siblings until next h2
    for h2 in soup.find_all("h2"):
        year_text = h2.get_text(strip=True)
        m = re.search(r"(19|20)\d{2}", year_text)
        year = m.group(0) if m else year_text

        for sib in h2.find_next_siblings():
            if sib.name == "h2":
                break
            if sib.name is None:
                continue

            # anchors on the sibling
            anchors = []
            if sib.name == "a" and sib.has_attr("href"):
                anchors = [sib]
            else:
                anchors = sib.find_all("a", href=True)

            for a in anchors:
                # guard the whole anchor processing so one bad anchor doesn't kill the loop
                try:
                    # debug: print only a short, safe summary instead of the full Tag
                    # safe_print("Debug anchor href:", a.get("href"))
                    href = urljoin(BASE, a["href"])

                    # Prefer h4 for title, fallback to h6 or anchor text
                    title_tag = a.find("h4") or a.find("h6")
                    if title_tag:
                        raw_title = title_tag.get_text(" ", strip=True)
                    else:
                        raw_title = a.get_text(" ", strip=True)

                    if not raw_title:
                        continue

                    # Normalize problematic characters (smart quotes, non-breaking spaces, etc.)
                    title = (
                        raw_title
                        .replace("\u201c", '"').replace("\u201d", '"')   # left/right double smart quotes
                        .replace("\u2018", "'").replace("\u2019", "'")  # left/right single smart quotes
                        .replace("\u00A0", " ")                         # NBSP -> space
                    )
                    # Remove control characters that would break JSON or console
                    title = re.sub(r"[\x00-\x1f\x7f]", "", title)

                    results.append({"year": year, "title": title, "url": href})
                except Exception as exc:
                    # log and continue on any per-anchor error
                    safe_print("Warning: failed to process anchor:", getattr(a, "href", "<no href>"), "error:", repr(exc))
                    continue

    # dedupe preserving order
    seen = set()
    deduped = []
    for item in results:
        key = (item["year"], item["title"], item["url"])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)

    return json.dumps(deduped, ensure_ascii=False)


def _clean_text(s: str) -> str:
    if s is None:
        return ''
    # unescape HTML entities
    s = html.unescape(s)
    # normalize common "smart" quotes and special spaces
    s = s.replace('\u201c', '"').replace('\u201d', '"')
    s = s.replace('\u2018', "'").replace('\u2019', "'")
    s = s.replace('\u2014', ' — ').replace('\u2013', '-')
    s = s.replace('\u00A0', ' ')
    # remove control characters
    s = re.sub(r'[\x00-\x1f\x7f]', '', s)
    # collapse whitespace
    s = re.sub(r'[ \t\v\f]+', ' ', s)
    s = re.sub(r'\s*\n\s*', '\n', s)
    s = s.strip()
    return s

@our_tools.tool
def get_talk_text(talk_url: str, timeout: int = 15) -> str:
    """
    Fetch a General Conference talk page by the url and return the talk text as plain text.

    Returns a single string containing:
      Title
      Byline (author/role)
      Kicker (if present)
      Body (section headers, paragraphs, list items) separated by blank lines.

    Example:
        text = get_talk_text("https://www.churchofjesuschrist.org/study/general-conference/2013/04/four-titles?lang=eng")
    """
    headers = {"User-Agent": "gc-talk-text-extractor/1.0 (+https://example.org)"}
    resp = requests.get(talk_url, headers=headers, timeout=timeout)
    resp.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(resp.text, "html.parser")

    # Prefer the structured article for General Conference talk pages
    article = (
        soup.find("article", {"data-content-type": "general-conference-talk"})
        or soup.find("article", id="main")
        or soup.find("article")
    )
    if article is None:
        # fallback: try to find the main content div
        article = soup.find("div", class_="body") or soup

    parts = []

    # Title
    title_tag = article.find("h1")
    if title_tag:
        parts.append(_clean_text(title_tag.get_text(" ", strip=True)))

    # Byline: author name / role
    author_name = article.find(class_="author-name") or article.find(attrs={"data-aid": re.compile(r"^2885.*author")})
    if author_name:
        parts.append(_clean_text(author_name.get_text(" ", strip=True)))
    author_role = article.find(class_="author-role")
    if author_role:
        parts.append(_clean_text(author_role.get_text(" ", strip=True)))

    # Kicker / intro
    kicker = article.find(class_="kicker")
    if kicker:
        parts.append(_clean_text(kicker.get_text(" ", strip=True)))

    # Body: try to select the structured "body-block" region used on the site
    body_block = article.select_one(".body-block") or article.find("div", class_="body") or article

    # Walk relevant tags in-source order and extract text
    # Keep headers (h2/h3/h4), paragraphs, and list items.
    collected = []
    for elem in body_block.find_all(["h2", "h3", "h4", "p", "li"], recursive=True):
        # skip navigation/notes refs that sometimes appear as anchors or superscripts
        # e.g., note-ref anchors are okay inside paragraphs but individual .note-ref elements alone are not desired
        if elem.name == "p":
            text = elem.get_text(" ", strip=True)
            if not text:
                continue
            # Skip tiny footnote-only paragraphs if they look like a numbered footnote marker only
            if re.fullmatch(r'^\s*\d+\s*$', text):
                continue
            collected.append(_clean_text(text))
        elif elem.name in ("h2", "h3", "h4"):
            header_text = elem.get_text(" ", strip=True)
            if header_text:
                # mark headers with surrounding newlines for readability
                collected.append(_clean_text(header_text).upper())
        elif elem.name == "li":
            li_text = elem.get_text(" ", strip=True)
            if li_text:
                collected.append("- " + _clean_text(li_text))

    # If body extraction failed, as a fallback collect all visible text under article (minus nav/footer)
    if not collected:
        # get visible text and split by paragraphs
        raw = article.get_text("\n", strip=True)
        for block in raw.splitlines():
            block = block.strip()
            if block:
                block = _clean_text(block)
                if block:
                    collected.append(block)

    # Combine header parts + collected body
    # Insert a blank line between logical blocks
    output_blocks = []
    if parts:
        output_blocks.append("\n".join(parts))
    if collected:
        output_blocks.append("\n\n".join(collected))

    return "\n\n".join(output_blocks)




class ChatAgent:
    def __init__(self, model: str, prompt: str, show_reasoning: bool, reasoning_effort: str | None):
        self._ai = AsyncOpenAI()
        self.model = model
        self.show_reasoning = show_reasoning
        self.reasoning: Reasoning = {}
        if show_reasoning:
            self.reasoning['summary'] = 'auto'
        if 'gpt-5' in self.model and reasoning_effort:
            match reasoning_effort:
                case "none" | "minimal" | "low" | "medium" | "high" | "xhigh":
                    self.reasoning["effort"] = reasoning_effort
                case _:
                    raise ValueError(f"Invalid reasoning effort: {reasoning_effort}")

        self.usage = []
        self.usage_markdown = format_usage_markdown(self.model, [])

        self._history = []
        self._prompt = prompt
        if prompt:
            self._history.append({'role': 'system', 'content': prompt})

    async def get_response(self, user_message: str):
        self._history.append({'role': 'user', 'content': user_message})

        while True:
            response = await self._ai.responses.create(
                input=self._history,
                model=self.model,
                reasoning=self.reasoning,
                tools=our_tools.tools
            )

            self.usage.append(response.usage)
            self.usage_markdown = format_usage_markdown(self.model, self.usage)
            self._history.extend(
                response.output
            )

            for item in response.output:
                if item.type == 'reasoning':
                    for chunk in item.summary:
                        yield 'reasoning', chunk.text

                elif item.type == 'function_call':
                    yield 'reasoning', f'{item.name}({item.arguments})'

                    print()
                    print()
                    print(f"===============================")
                    print(f"Debugging: The model requested a function called {item.name} with arguments {item.arguments}.")
                    print(f"===============================")

                    func = our_tools.get_tool_function(item.name)
                    args = json.loads(item.arguments)
                    result = func(**args) # type: ignore
                    self._history.append({
                        'type': 'function_call_output',
                        'call_id': item.call_id,
                        'output': str(result)
                    })
                    yield 'reasoning', str(result)

                elif item.type == 'message':
                    for chunk in item.content:
                        txt = getattr(chunk, 'text', None)
                        if txt is not None:
                            yield 'output', txt
                        else:
                            # handle common non-text chunk shapes (refusal/tool/etc.)
                            # try common fields, then fallback to string
                            reason = getattr(chunk, 'reason', None) or getattr(chunk, 'refusal', None)
                            if reason is not None:
                                yield 'output', f'[refusal: {reason}]'
                            else:
                                yield 'output', str(chunk)
                    return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print_usage(self.model, self.usage)


async def _main_console(agent_args):
    with ChatAgent(**agent_args) as agent:
        while True:
            message = input('User: ')
            if not message:
                break

            reasoning_complete = True
            if agent.show_reasoning:
                print(' Reasoning '.center(30, '-'))
                reasoning_complete = False

            async for text_type, text in agent.get_response(message):
                if text_type == 'output' and not reasoning_complete:
                    print()
                    print('-' * 30)
                    print()
                    print('Agent: ')
                    reasoning_complete = True

                print(text, end='', flush=True)
            print()
            print()


def _main_gradio(agent_args):
    # Constrain width with CSS and center
    css = """
    /* limit overall Gradio app width and center it */
    .gradio-container, .gradio-app, .gradio-root {
      width: 120ch;
      max-width: 120ch !important;
      margin-left: auto !important;
      margin-right: auto !important;
      box-sizing: border-box !important;
    }
    
    #reasoning-md {
        max-height: 300px;
        overflow-y: auto;
    }
    """

    reasoning_view = gr.Markdown('', elem_id='reasoning-md')
    usage_view = gr.Markdown('')

    with gr.Blocks(css=css, theme=gr.themes.Monochrome()) as demo: # type: ignore
        agent = gr.State()

        async def get_response(message, chat_view_history, agent):
            output = ""
            reasoning = ""

            async for text_type, text in agent.get_response(message):
                if text_type == 'reasoning':
                    reasoning += text
                elif text_type == 'output':
                    output += text
                else:
                    raise NotImplementedError(text_type)

                yield output, reasoning, agent.usage_markdown, agent

            yield output, reasoning, agent.usage_markdown, agent

        with gr.Row():
            with gr.Column(scale=5):
                bot = gr.Chatbot(
                    label=' ',
                    height=600,
                    resizable=True,
                )
                chat = gr.ChatInterface(
                    chatbot=bot,
                    fn=get_response,
                    additional_inputs=[agent],
                    additional_outputs=[reasoning_view, usage_view, agent]
                )

            with gr.Column(scale=1):
                reasoning_view.render()
                usage_view.render()

        demo.load(fn=lambda: ChatAgent(**agent_args), outputs=[agent])

    demo.launch()


def main(prompt_path: Path, model: str, show_reasoning, reasoning_effort: str | None, use_web: bool):
    agent_args = dict(
        model=model,
        prompt=prompt_path.read_text() if prompt_path else '',
        show_reasoning=show_reasoning,
        reasoning_effort=reasoning_effort

    )

    if use_web:
        _main_gradio(agent_args)
    else:
        asyncio.run(_main_console(agent_args))


# Launch app
if __name__ == "__main__":
    parser = argparse.ArgumentParser('ChatBot')
    parser.add_argument('prompt_file', nargs='?', type=Path, default=None)
    parser.add_argument('--web', action='store_true')
    parser.add_argument('--model', default='gpt-5-nano')
    parser.add_argument('--show-reasoning', action='store_true')
    parser.add_argument('--reasoning-effort', default='low')
    args = parser.parse_args()
    main(args.prompt_file, args.model, args.show_reasoning, args.reasoning_effort, args.web)
