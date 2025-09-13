import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROMPT_ID = os.getenv('PROMPT_ID')

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

response = client.responses.create(
  prompt={
    "id": PROMPT_ID,
    "version": "1"
  }
)

import tiktoken

def count_tokens_with_model(text: str, model: str = "gpt-4.1-nano") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
