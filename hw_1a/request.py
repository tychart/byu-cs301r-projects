import os
from dotenv import load_dotenv
from time import time
from openai import Client

from usage import print_usage

def openai_client():
    load_dotenv()
    return Client(api_key=os.getenv('OPENAI_API_KEY'))
    
def ollama_client():
    return Client(
        base_url="http://192.168.10.35:11434/v1",
        api_key="ollama"
    )

def main():
    start = time()

    modelnum = 2

    match modelnum:
        case 1:
            model = "gpt-5-nano"
        case 2:
            model = "gemma3:4b"
        case 3:
            model = "gpt-oss"

    if "gpt" in model and model != "gpt-oss":
        client = openai_client()
    else:
        client = ollama_client()


    input_text = f"""
Please output detailed and exact ascii art in the shape of a bird:


"""
    
    file_path = 'test_onlyalpahanum.txt'

    with open(file_path, 'r') as file:
        file_content = file.read()


# #     input_text = f"""
# # Please take the following text as input, and output what you think the purpose of the text document is:

# # {file_content}

# """
    
    
    response = client.responses.create(
        model=model,
        input=input_text,
        reasoning={'effort': 'low'}
    )

    # print(f"Full Response: {response}")

    print("-------------------------------------------")
    print("Response:")
    print(response.output_text)
    print("-------------------------------------------")


    print(f'Took {round(time() - start, 2)} seconds')
    print_usage(model, response.usage)
    


if __name__ == '__main__':
    main()
