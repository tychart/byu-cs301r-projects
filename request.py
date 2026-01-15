import os
from dotenv import load_dotenv
from time import time
from openai import Client

from usage import print_usage

def openai_client():
    load_dotenv()
    print(f"Key: {os.getenv('OPENAI_APIKEY')}")
    return Client(api_key=os.getenv('OPENAI_APIKEY'))
    
def ollama_client():
    return Client(
        base_url="http://192.168.10.35:11434/v1",
        api_key="ollama"
    )

def main():
    modelenv = 3
    # client = openai_client()
    client = ollama_client()
    start = time()
    # model = "gpt-5-nano"
    model = "gemma3:4b"
    
    response = client.responses.create(
        model=model,
        input="Hi.",
        # reasoning={'effort': 'low'}
    )

    print(f'Took {round(time() - start, 2)} seconds')
    print_usage(model, response.usage)
    print(response.output_text)


if __name__ == '__main__':
    main()
