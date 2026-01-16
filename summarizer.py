import os
from groq import Groq
from dotenv import load_dotenv
import asyncio
from typing import List
from scraper import extract_oil_gas_news
from ollama import chat
from ollama import ChatResponse

load_dotenv()

# async def summarize_news(news):
#     client = Groq()
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Create a point wise compact summary based on the Headings and Short_description:\n\n" + str(
#                     news),
#             }
#         ],
#         model="llama-3.3-70b-versatile",
#     )
#     return chat_completion.choices[0].message.content


async def summarize_news(news):
    # response: ChatResponse = chat(model='qwen3:0.6b', messages=[
    response: ChatResponse = chat(model='gpt-oss:120b-cloud', messages=[
        {
            "role": "user",
            "content": "Create a point wise compact short summary based on the Headings and Short_description:\n\n" + str(
                    news),
        },
    ])

    return response.message.content

if __name__ == "__main__":
    news,links = asyncio.run(extract_oil_gas_news())
    # print(news,links)
    summary = asyncio.run(summarize_news(news))
    print("Summary:\n", summary)