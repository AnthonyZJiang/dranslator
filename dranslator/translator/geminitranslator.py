import json

import os
from google import genai
from google.genai import types, errors


GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
SYS_INSTRUCTION = """将关于美股交易的英语翻译为中文。只回复翻译内容"""
MODEL = os.getenv("DRANSLATOR_LLM_MODEL", "gemini-2.0-flash-lite")


client = genai.Client(api_key=GEMINI_API_KEY)

generate_content_config = types.GenerateContentConfig(
    system_instruction=[
        types.Part.from_text(text=SYS_INSTRUCTION),
    ],
)

def translate(input: str):
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=input),
            ],
        ),
    ]

    try:
        chunks = [c for c in client.models.generate_content_stream(
            model=MODEL,
            contents=contents,
            config=generate_content_config,
        )]
        
        text = ''.join([c.text for c in chunks])
        return {
            'translation': text
        }
    except errors.APIError as e:
        # Handle specific error codes
        if e.code == 403:
            return {
                'error': f'Permission denied (403): {e.message}'
            }
        elif e.code == 429:
            return {
                'error': f'Rate limit exceeded (429): {e.message}'
            }
        else:
            # Handle other API errors
            return {
                'error': f'API Error ({e.code}): {e.message}'
            }
    except json.JSONDecodeError:
        return {
            'error': 'JSON decode error'
        }
    except Exception as e:
        # Catch any other unexpected errors
        return {
            'error': f'Unexpected error: {e}'
        }

def limit_reached() -> bool:
    return False
