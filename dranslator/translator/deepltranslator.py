import os
from deepl import DeepLClient, DeepLException


DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')
DEEPL_GLOSSARY_ID = os.getenv('DEEPL_GLOSSARY_ID', None)
TRANSLATE_TO_LANGUAGE = os.getenv('TRANSLATE_TO_LANGUAGE').upper()
TRANSLATE_FROM_LANGUAGE = os.getenv('TRANSLATE_FROM_LANGUAGE').upper()


deepl_client = DeepLClient(DEEPL_API_KEY)

def translate(text: str, from_language: str = TRANSLATE_FROM_LANGUAGE, to_language: str = TRANSLATE_TO_LANGUAGE) -> dict[str, str]:
    try:
        result = deepl_client.translate_text(text, source_lang=from_language, target_lang=to_language, glossary=DEEPL_GLOSSARY_ID)
        return {
            'translation': result.text
        }
    except DeepLException as e:
        # TODO: error handling https://developers.deepl.com/docs/best-practices/error-handling
        if e.http_status_code == 429:
            return {
                'error': 'Rate limit exceeded'
            }
        elif e.http_status_code == 456:
            return {
                'error': 'Quota exceeded'
            }
        elif e.http_status_code == 500:
            return {
                'error': 'Internal server error'
            }
        else:
            return {
                'error': str(e)
            }

def limit_reached() -> bool:
    usage = deepl_client.get_usage()
    return usage.any_limit_reached
