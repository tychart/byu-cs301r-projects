import argparse
import os
from pathlib import Path
from dotenv import load_dotenv
from time import time
from openai import Client
import sys

# Adds the above directory to the syspath for shared package
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.usage import print_usage



def openai_client():
    load_dotenv()
    return Client(api_key=os.getenv('OPENAI_API_KEY'))
    
def ollama_client():
    return Client(
        base_url='http://192.168.10.35:11434/v1',
        api_key='ollama'
    )



def main():
    
    modelnum = 1

    prompt = """
4. Logic Puzzle: A man has 53 socks in his drawer: 21 identical blue, 15 identical black and 17 identical red. The lights are out, and he is completely in the dark. How many socks must he take out to make 100 percent certain he has at least one pair of black socks?

Show your thinking and reasoning, then provide an answer
"""

    match modelnum:
        case 1:
            model = 'gpt-5-nano'
        case 2:
            model = 'gemma3:4b'
        case 3:
            model = 'llama3.1:8b'
        case 4:
            model = 'gpt-oss'
        case 5:
            model = 'gpt-3.5-turbo'

    if 'gpt' in model and model != 'gpt-oss':
        client = openai_client()
    else:
        client = ollama_client()

    print(f"Running with model {model}")


    response = client.responses.create(
        model=model,
        input=prompt,
        reasoning={'effort': 'low'}
    )

    print(f'Response: {response}')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('AI Response')

    # parser.add_argument(
    #     '-p', '--prompt-file',
    #     metavar='PROMPT_FILE',
    #     type=Path,
    #     required=True,
    #     help='Path to the file containing the prompt'
    # )

    # # parser.add_argument(
    # #     'input_text',
    # #     help='Text input to feed to the AI'
    # # )

    # parser.add_argument(
    #     '--model',
    #     default='2',
    #     type=int,
    #     help='Model number (1-4) 1=gpt-5-nano, 2=gemma3, 3=gpt-oss'
    # )

    # args = parser.parse_args()

    # print(args)

    main()
