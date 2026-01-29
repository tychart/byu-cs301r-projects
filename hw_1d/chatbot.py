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


# def openai_client():
#     load_dotenv()
#     return Client(api_key=os.getenv('OPENAI_APIKEY'))
    
# def ollama_client():
#     return Client(
#         base_url='http://192.168.10.35:11434/v1',
#         api_key='ollama'
#     )

class ChatAgent:
    def __init__(self, model: str, prompt: str):
        load_dotenv()
        self._ai = AsyncOpenAI(api_key=os.getenv('OPENAI_APIKEY'))
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
            # reasoning=self.reasoning
        )
        self.usage.append(response.usage)
        self._history.extend(
            response.output
        )
        return response.output_text

    def reset(self):
        # Reset conversation back to just the system prompt
        self._history = []
        if self._prompt:
            self._history.append({'role': 'system', 'content': self._prompt})
        self.usage = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print_usage(self.model, self.usage)


async def _main_console(agent):
    while True:
        message = input('User: ')
        if not message:
            break
        # response = await agent.get_response(message, None)
        response = await agent.get_response(message)
        print('Agent:', response)


def _main_gradio(agent, share: bool):
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

        
        def do_reset():
            agent.reset()
            # Clear chatbot UI + reset usage panel
            return [], format_usage_markdown(agent.model, [])

        with gr.Row():
            with gr.Column(scale=5):
                with gr.Row():
                    reset_btn = gr.Button("Reset conversation")

                bot = gr.Chatbot(
                    label=" ",
                    height=600,
                    resizable=True,
                )
                chat = gr.ChatInterface(
                    chatbot=bot,
                    fn=get_response,
                    additional_outputs=[usage_view],
                )

                reset_btn.click(
                    fn=do_reset,
                    outputs=[bot, usage_view],
                )

            with gr.Column(scale=1):
                usage_view.render()


    demo.launch(share=share)


def main(prompt_path: Path, model: str, use_web: bool, share: bool):
    with ChatAgent(model, prompt_path.read_text() if prompt_path else '') as agent:
        if use_web:
            _main_gradio(agent, share)
        else:
            asyncio.run(_main_console(agent))


# Launch app
if __name__ == "__main__":
    parser = argparse.ArgumentParser('ChatBot')
    parser.add_argument('prompt_file', nargs='?', type=Path, default=None)
    parser.add_argument('--web', action='store_true')
    parser.add_argument('--model', default='gpt-5-nano')
    parser.add_argument('--share', action='store_true')
    args = parser.parse_args()
    main(args.prompt_file, args.model, args.web, args.share)
