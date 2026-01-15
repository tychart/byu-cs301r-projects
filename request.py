import os
from dotenv import load_dotenv
from time import time
from openai import Client

from usage import print_usage

def openai_client():
    load_dotenv()
    return Client(api_key=os.getenv('OPENAI_APIKEY'))
    
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



    
    
    response = client.responses.create(
        model=model,
        input="Given the following list, can you please classify the following cities by if they are over or under 100,000 people?\n\nList: ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']\n\nOutput: Over 100,",
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
