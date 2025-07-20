import logging
import os
import dotenv
from azure.core.exceptions import HttpResponseError
from azure.core.credentials import AzureKeyCredential
from azure.ai.translation.text import TextTranslationClient

dotenv.load_dotenv()

AZURE_TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY')
AZURE_TRANSLATOR_REGION = os.getenv('AZURE_TRANSLATOR_REGION')
TRANSLATE_FROM_LANGUAGE = os.getenv('TRANSLATE_FROM_LANGUAGE')
TRANSLATE_TO_LANGUAGE = os.getenv('TRANSLATE_TO_LANGUAGE')

logger = logging.getLogger(__name__)

credential = AzureKeyCredential(AZURE_TRANSLATOR_KEY)
client = TextTranslationClient(credential=credential, region=AZURE_TRANSLATOR_REGION)

def translate(text: str, from_language: str=TRANSLATE_FROM_LANGUAGE, to_language: str=TRANSLATE_TO_LANGUAGE) -> dict[str, str]: 
    try:
        response = client.translate(body=[text], to_language=[to_language], from_language=from_language)
        
        return {
            'translation': response[0].translations[0].text
        }
    
    except HttpResponseError as e:
        logger.error(f"Error translating text: {e}")
        return {
            'error': str(e.error.code) + ': ' + str(e.error.message)
        }

if __name__ == '__main__':
    print(translate('Hello, world!'))