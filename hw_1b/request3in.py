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

def send_request(client, prompt, model='gemma3'):
    start = time()
    
    response = client.responses.create(
        model=model,
        input=prompt,
        reasoning={'effort': 'low'}
    )

    print(f'Took {round(time() - start, 2)} seconds')

    return response


def main(modelnum: int, prompt: str, out_format: str, in_text: str):
    

    modelnum = 2

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


#     input_text = f"""
# Please output detailed and exact ascii art in the shape of a bird:


# """
    
#     file_path = 'test_onlyalpahanum.txt'

#     with open(file_path, 'r') as file:
#         file_content = file.read()


# #     input_text = f"""
# # Please take the following text as input, and output what you think the purpose of the text document is:

# # {file_content}

# """

    input_text = f'{prompt}\n# **{in_text}**\n\n{out_format}\n---\n\n'
    # print(f'input_text: {input_text}')
    response = send_request(client, model=model, prompt=input_text)

    # print(f'Full Response: {response}')

    print('-------------------------------------------')
    print('Response:')
    print(response.output_text)
    print('-------------------------------------------')


    
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

    parser.add_argument('--model', default='gemma3')
    args = parser.parse_args()

    # print(args)

    main(args.model, args.prompt_file.read_text(), args.output_format_file.read_text(), args.input_text)
