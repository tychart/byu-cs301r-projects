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
    return Client(api_key=os.getenv('OPENAI_APIKEY'))
    
def ollama_client():
    return Client(
        base_url='http://192.168.10.35:11434/v1',
        api_key='ollama'
    )

# def send_request(client, prompt, model):
#     start = time()
    
#     response = client.responses.create(
#         model=model,
#         input=prompt,
#         reasoning={'effort': 'low'}
#     )

#     print(f'Took {round(time() - start, 2)} seconds')

#     return response


def main(modelnum: int, prompt: str):
    
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

    # input_text = f'{prompt}\n# **{in_text}**\n\n{out_format}\n---\n\n'
    # print(f'input_text: {input_text}')
    

    # print(f'Full Response: {response}')

    # print('-------------------------------------------')
    # print('Response:')
    # print(response.output_text)
    # print('-------------------------------------------')


    
    # print_usage(model, response.usage)

    times: list[float] = []
    input_tokens: list[int] = []
    output_tokens: list[int] = []
    reasoning_tokens: list[int] = []
    

    for i in range(0, 10):
        
        start = time()
    
        response = client.responses.create(
            model=model,
            input=prompt,
            reasoning={'effort': 'low'}
        )

        times.append(time() - start)

        if (response.usage == None):
            raise Exception('Usage is none')
        

        input_tokens.append(response.usage.input_tokens)
        output_tokens.append(response.usage.output_tokens)

        if (response.usage.output_tokens_details != None):
            reasoning_tokens.append(response.usage.output_tokens_details.reasoning_tokens)

        print(f'Loop index {i} took {round(times[-1], 2)} seconds')

        # print(response.usage)
    
    print('----------------------------------------------------')
    print(f'Average time: {round(sum(times) / len(times), 3)} seconds')
    print(f'Average input tokens: {round(sum(input_tokens) / len(input_tokens), 3)}')
    print(f'Average output tokens: {round(sum(output_tokens) / len(output_tokens), 3)}')
    print(f'Average tokens per second: {round(sum(input_tokens) / len(input_tokens), 3)}')
    
    if (len(reasoning_tokens) > 0):
        print(f'Average reasoning tokens: {round(sum(reasoning_tokens) / len(reasoning_tokens), 3)}')
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser('AI Response')

    parser.add_argument(
        '-p', '--prompt-file',
        metavar='PROMPT_FILE',
        type=Path,
        required=True,
        help='Path to the file containing the prompt'
    )

    parser.add_argument(
        '-e', '--effort',
        type=str,
        default='low',
        help="Can be 'low', 'medium', or 'high'" 
    )

    # parser.add_argument(
    #     'input_text',
    #     help='Text input to feed to the AI'
    # )

    parser.add_argument(
        '--model',
        default='2',
        type=int,
        help='Model number (1-4) 1=gpt-5-nano, 2=gemma3, 3=gpt-oss'
    )

    args = parser.parse_args()

    # print(args)

    main(args.model, args.prompt_file.read_text())
