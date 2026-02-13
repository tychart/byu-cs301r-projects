# Before running this script:
# pip install gradio openai

import os
import argparse
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv
import gradio as gr
from openai import AsyncOpenAI

# Adds the above directory to the syspath for shared package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.usage import print_usage, format_usage_markdown

from chroma_demo import query_whole_documents


# def openai_client():
#     load_dotenv()
#     return Client(api_key=os.getenv('OPENAI_API_KEY'))
    
# def ollama_client():
#     return Client(
#         base_url='http://192.168.10.35:11434/v1',
#         api_key='ollama'
#     )

class ChatAgent:
    def __init__(self, model: str, prompt: str):
        load_dotenv()
        self._ai = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.usage = []
        self.model = model
        self.reasoning = {'effort': 'low'}
        self._prompt = prompt
        self._history = []
        if prompt:
            self._history.append({'role': 'system', 'content': prompt})

    async def get_response(self, user_message: str):
        self._history.append({'role': 'user', 'content': user_message})

        response = await self._ai.responses.create(
            input=self._history,
            model=self.model,
            reasoning=self.reasoning
        )
        self.usage.append(response.usage)
        self._history.extend(
            response.output
        )
        return response.output_text

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # pirnt_usage(self.model, self.usage)
        print("Exiting")


async def _main_console(agent):
    while True:
        message = input('User: ')
        if not message:
            break
        # response = await agent.get_response(message, None)

        docs = query_whole_documents(
            collection="confrence",
            chroma_dir="./db",
            query=message,
            n_results=2,            
        )

        prompt = "The following documents are relevent to the question asked by the user:\n\n"

        for doc in docs:
            prompt += "Document 1:\n"
            for chunk in doc:
                prompt += chunk
            prompt += "\n\n"
        prompt += "This is the user's query:\n\n"

        prompt += message

        response = await agent.get_response(prompt)
        print('Agent:', response)


def _main_gradio(agent):
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
    """

    usage_view = gr.Markdown(format_usage_markdown(agent.model, []))

    with gr.Blocks(css=css, theme=gr.themes.Monochrome()) as demo:
        async def get_response(message, chat_view_history):
            response = await agent.get_response(message)
            usage_content = format_usage_markdown(agent.model, agent.usage)
            return response, usage_content

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
                    additional_outputs=[usage_view]
                )

            with gr.Column(scale=1):
                usage_view.render()

    demo.launch()


def main(prompt_path: Path, model: str, use_web: bool):
    with ChatAgent(model, prompt_path.read_text() if prompt_path else '') as agent:
        if use_web:
            _main_gradio(agent)
        else:
            asyncio.run(_main_console(agent))


# Launch app
if __name__ == "__main__":
    parser = argparse.ArgumentParser('ChatBot')
    parser.add_argument('prompt_file', nargs='?', type=Path, default=None)
    parser.add_argument('--web', action='store_true')
    parser.add_argument('--model', default='gpt-5-nano')
    args = parser.parse_args()
    main(args.prompt_file, args.model, args.web)
