import argparse
import os
import re
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from time import time
from openai import Client
import sys
import json
import json5

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

def send_request(client, prompt, model='gemma3'):
    start = time()
    
    response = client.responses.create(
        model=model,
        input=prompt,
        reasoning={'effort': 'low'}
    )

    print(f'Took {round(time() - start, 2)} seconds')

    return response

def parse_llm_json(llm_text: str):
    """
    Tries to extract JSON from LLM output and parse it.
    Returns a dictionary or None if parsing fails.
    """
    try:
        # 1. Try strict JSON first
        return json.loads(llm_text)
    except json.JSONDecodeError:
        pass

    try:
        # 2. Use JSON5 for forgiving parsing
        data = json5.loads(llm_text)
    except Exception as e:
        # 3. Try to extract first {...} block with regex
        match = re.search(r"\{.*\}", llm_text, re.DOTALL)
        if match:
            try:
                data = json5.loads(match.group())
            except Exception as e2:
                print("Failed to parse LLM JSON:", e2)
                return None
        else:
            print("No JSON-like content found in LLM response")
            return None

    return data



def main(modelnum: int, prompt: str, out_format: str, in_text: str):
    

    # modelnum = 2

    match modelnum:
        case 1:
            model = 'gpt-5-nano'
        case 2:
            model = 'gemma3:4b'
        case 3:
            model = 'gpt-oss'

    if 'gpt' in model and model != 'gpt-oss':
        client = openai_client()
    else:
        client = ollama_client()


    input_text = f'{prompt}\n# **{in_text}**\n\n{out_format}\n---\n\n'
    # print(f'input_text: {input_text}')
    response = send_request(client, model=model, prompt=input_text)

    
    # print(response.output[0].)

    # print(f'Full Response: {response}')

    print('-------------------------------------------')
    print('Response:')
    print(response.output_text)
    print('-------------------------------------------')

    print("Trying to parse to JSON:")
    print(parse_llm_json(response.output_text))

    
    print_usage(model, response.usage)
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('AI Response')
    parser.add_argument(
        '-o', '--output-format-file',
        metavar='PATH_TO_FILE',
        type=Path,
        help='Path to the file where output will be saved'
    )

    parser.add_argument(
        '-p', '--prompt-file',
        metavar='PROMPT_FILE',
        type=Path,
        help='Path to the file containing prompts'
    )

    parser.add_argument(
        'input_text',
        help='Text input to feed to the AI'
    )

    parser.add_argument('--model', default=2, type=int)
    args = parser.parse_args()

    print(args)

    if (args.output_format_file):
        main(
            args.model,
            args.prompt_file.read_text(),
            args.output_format_file.read_text(),
            args.input_text
        )
    else:
        main(
            args.model,
            args.prompt_file.read_text(),
            "",
            args.input_text
        )
