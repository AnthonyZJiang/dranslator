import logging
import os
import dotenv
import requests
import uuid

dotenv.load_dotenv()

AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')
AZURE_TRANSLATOR_LOCATION = os.getenv('AZURE_TRANSLATOR_LOCATION')
TRANSLATE_FROM_LANGUAGE = os.getenv('TRANSLATE_FROM_LANGUAGE')
TRANSLATE_TO_LANGUAGE = os.getenv('TRANSLATE_TO_LANGUAGE')

logger = logging.getLogger(__name__)


def azure_translate(payload: list[dict[str, str]], from_language: str=TRANSLATE_FROM_LANGUAGE, to_language: str=TRANSLATE_TO_LANGUAGE) -> dict[str, str]:
    """
    Translate a list of text using Azure Translator API.
    
    Args:
        payload: A list of dictionaries containing the text to translate. 
                 Example:
                 [{
                     'text': 'The text to translate.'
                 }]
        from_language: The language of the text to translate from.
        to_language: The language to translate the text to.
        
    Returns:
        A dictionary containing the translated text.
        Example:
        {
            'translations': [
                'The translated text.'
            ]
            'error': 'The error message if the translation fails.'
        }
    """
    
    if not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_LOCATION:
        return {
            'error': 'Azure Translator API details missing.'
        }
    api_url = 'https://api.cognitive.microsofttranslator.com/translate'

    params = {
        'api-version': '3.0',
        'from': from_language,
        'to': to_language
    }

    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_TRANSLATOR_LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }
    request = requests.post(api_url, params=params, headers=headers, json=payload, timeout=10)
    response = request.json()

    if not response:
        return {
            'error': 'No response from Azure Translator'
        }
    if isinstance(response, dict):
        if response.get('error', None):
            return {
                'error': f'{response["error"]["code"]}: {response["error"]["message"]}'
            }
    if isinstance(response, list):
        return {
            'translations': [r['translations'][-1]['text'] for r in response]
        }
    return {
        'translations': [response['translations'][-1]['text']]
    }

if __name__ == '__main__':
    print(azure_translate([{'text': 'Hello, world!'}]))