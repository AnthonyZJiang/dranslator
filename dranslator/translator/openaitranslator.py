import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROMPT_ID = os.getenv('PROMPT_ID')
MODEL = os.getenv("DRANSLATOR_LLM_MODEL", "gpt-5-nano")

client = OpenAI(
    api_key=OPENAI_API_KEY,
)


def translate(input: str):
    try:
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
                },
                "verbosity": "low"
                    },
            reasoning={
                "effort": "minimal"
            },
            tools=[],
            store=True,
            include=[
            ]
        )
    except Exception as e:
        return {
            'error': str(e)
        }
    if response.error:
        return {
            'error': response.error.message
        }
    return {
        'translation': response.output_text
    }
