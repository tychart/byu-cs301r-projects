import openai
import numpy as np
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import asyncio

from chonkie import TokenChunker

# client = openai.AsyncOpenAI()

def openai_client():
    load_dotenv()
    return openai.AsyncOpenAI(api_key=os.getenv('OPENAI_APIKEY'))
    
def ollama_client():
    return openai.AsyncOpenAI(
        base_url='http://192.168.10.35:11434/v1',
        api_key='ollama'
    )

async def embed(client, content: list[str]) -> np.array:
    response = await client.embeddings.create(
        input=content,
        model='text-embedding-3-small'
    )
    return np.array([emb.embedding for emb in response.data])

async def get_verses(client, content_embeds, context_verses, phrase, threshold = 0.6):
    embedding = await embed(client, [phrase])
    scores = content_embeds @ embedding.T
    return np.array(context_verses)[scores.flatten() > threshold]


async def embed_token_batched(client, chunks, token_budget=250_000):
    all_vecs = []
    batch, tok = [], 0

    async def flush(batch_texts):
        resp = await client.embeddings.create(model="text-embedding-3-small", input=batch_texts)
        return [d.embedding for d in resp.data]

    for ch in chunks:
        print(f"chunk {len(batch)} / {len(chunks)}")
        t = ch.token_count
        if batch and tok + t > token_budget:
            all_vecs.extend(await flush(batch))
            batch, tok = [], 0
        batch.append(ch.text)
        tok += t

    if batch:
        all_vecs.extend(await flush(batch))

    return np.array(all_vecs)


async def main():

    # chunker = RecursiveChunker()

    chunker = TokenChunker(
        tokenizer="character",
        chunk_size=512,
        chunk_overlap=50
    )


    local = False

    if local:
        client = ollama_client()
    else:
        client = openai_client()

    # phrases = [
    #     'hello', 'hi', 'good-bye', 'see ya later', 'moose', '1 + 1 = 2', '2 + 2 = 5', 'qperqoweirupqweor',
    #     '!@#$%^&*()_', 'def foobar(): return 7', 'specificity', 'agent engineering', 
    #     'Utah'
    # ]

    # response = await client.embeddings.create(
    #     input=phrases,
    #     model='text-embedding-3-small'
    # )

    # embeds = np.array([emb.embedding for emb in response.data])


    # phrase = 'hola'
    # query = await embed(client, phrase)

    # ax = plt.bar(x=range(len(phrases)), height=(query @ embeds.T))
    # plt.xticks(range(len(phrases)), phrases, rotation=45, ha='right', rotation_mode='anchor')
    # plt.title('Embedding similiarity for ' + phrase)
    # plt.ylim([0, 1]);
    # plt.show()

    with open('shakespeare.txt', 'r') as file:
        text = file.read()

    print("Currently chunking...")
    chunks = chunker(text)
    print("Finished chunking")


    # print(chunks)

    chunk_list = []

    for chunk in chunks:
        # print(f"Chunk: {chunk.text}")
        # print(f"Tokens: {chunk.token_count}")
        chunk_list.append(chunk.text)

    # print(chunk_list)

    # content_embeds = await embed(client, chunk_list)

    print("Currently embedding...")
    content_embeds = await embed_token_batched(client, chunks)
    print("Finished embedding")


    hits = await get_verses(
        client, 
        content_embeds,
        chunk_list, 
        'bible', 
        # threshold=0.32
        threshold=0.2
    )

    print(f"Hits: {len(hits)}")

    for hit in hits:
        print(hit)
        print("--------------------------------------")

if __name__ == '__main__':
    asyncio.run(main())
