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
                    "role": "developer",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "做为一名翻译机器人，将涉及美股交易的内容翻译为中文，保持专业术语准确且通顺自然。确保在翻译之前理解原文。仅输出译文及（如有必要）极精炼的译注说明，不输出提示或额外解释。"
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": input
                        }
                    ]
                },
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
