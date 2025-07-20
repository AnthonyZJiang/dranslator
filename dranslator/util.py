import re
import logging
from logging.handlers import TimedRotatingFileHandler
from discord.utils import _ColourFormatter
import os


def setup_logging(log_file: str = None) -> logging.Handler:
    level = logging.DEBUG
    
    library, _, _ = __name__.partition('.')
    logger = logging.getLogger(library)
    logger.setLevel(level)

    # Stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    formatter = _ColourFormatter()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    # File handler
    if not log_file:
        return stream_handler
    
    if not os.path.exists(os.path.dirname(log_file)):
        os.makedirs(os.path.dirname(log_file))
        
    file_handler_info = TimedRotatingFileHandler(log_file, when='D', interval=1, backupCount=7)
    file_handler_info.setLevel(logging.INFO)
    f_format = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s::%(module)s %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler_info.setFormatter(f_format)
    
    file_handler_debug = TimedRotatingFileHandler(log_file.rstrip('.log') + '_debug.log', when='D', interval=1, backupCount=7)
    file_handler_debug.setLevel(logging.DEBUG)
    f_format = logging.Formatter('%(asctime)s %(levelname)-8s %(name)s::%(module)s %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler_debug.setFormatter(f_format)
    
    logger.addHandler(file_handler_info)
    logger.addHandler(file_handler_debug)
    
    return stream_handler


def is_ticker_only(text: str) -> bool:
    return re.match(r'^\$?[A-z]{1,5}$', text.strip()) is not None

def is_punctuation_only(text: str) -> bool:
    return re.match(r'^[^\w\s]+$', text.strip()) is not None

def is_mostly_chinese(text: str, threshold: float = 0.5) -> bool:
    """
    Check if a text mostly contains Chinese characters.
    
    Args:
        text: The text to check
        threshold: Minimum percentage of Chinese characters to consider as "mostly Chinese" (default: 0.5 = 50%)
        
    Returns:
        bool: True if the text is mostly Chinese characters, False otherwise
    """
    if not text or not text.strip():
        return False
        
    # Remove whitespace and punctuation for more accurate counting
    cleaned_text = re.sub(r'[\s\W_]', '', text, flags=re.UNICODE)
    
    if not cleaned_text:
        return False
        
    # Count Chinese characters (CJK Unified Ideographs)
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', cleaned_text)
    chinese_count = len(chinese_chars)
    
    # Calculate percentage
    total_chars = len(cleaned_text)
    chinese_percentage = chinese_count / total_chars
    
    return chinese_percentage >= threshold