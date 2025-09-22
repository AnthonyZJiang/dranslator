import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROMPT_ID = os.getenv('PROMPT_ID')
MODEL = os.getenv("DRANSLATOR_LLM_MODEL", "gpt-5-nano")

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


def translate(input: str):
    response = client.responses.create(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": "将关于美股交易的英语翻译为中文。只回复翻译内容:\n" + input
                    }
                ]
            }
        ],
        text={
            "format": {
                "type": "text"
            }
        },
        reasoning={},
        tools=[],
        temperature=1,
        max_output_tokens=2048,
        top_p=1,
        store=True,
        include=["web_search_call.action.sources"]
    )
    if response.error:
        return {
            'error': response.error.message
        }
    return {
        'translation': response.output_text
    }


    # import tiktoken

    # def count_tokens_with_model(text: str, model: str = MODEL) -> int:
    #     encoding = tiktoken.encoding_for_model(model)
    #     return len(encoding.encode(text))
