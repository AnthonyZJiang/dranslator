import logging
import re
import json
import os
import hashlib
import dotenv
import discord

from .util import setup_logging, is_mostly_chinese, is_ticker_only, is_punctuation_only

dotenv.load_dotenv()
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TRIGGER_EMOJI = os.getenv('TRIGGER_EMOJI')
TRANSLATOR = os.getenv('TRANSLATOR')

if TRANSLATOR == 'deepl':
    from .translator.deepltranslator import translate
elif TRANSLATOR == 'gemini':
    from .translator.geminitranslator import translate
elif TRANSLATOR == 'azure':
    from .translator.azuretranslator import translate
elif TRANSLATOR == 'openai':
    from .translator.openaitranslator import translate
else:
    raise ValueError(f"Invalid translator: {TRANSLATOR}")

stream_handler = setup_logging()
logger = logging.getLogger(__name__)


class MessagePreProcessor:
    def __init__(self, message: str, config: dict):
        self.message = message
        self.lines = message.split('\n')
        self.config = config
    
    def preprocess(self, expand_abbreviations: bool = True) -> str:
        lines = [line for line in self.lines if not self._is_reply_to(line) and not self._is_delay_note(line)]
        self.message = '\n'.join(lines)
        self._remove_links()
        if expand_abbreviations:
            self._expand_abbreviations()
        self._remove_discord_commands()
        return self.message
    
    def _remove_discord_commands(self) -> None:
        # remove timestamp <t:1231245> <t:1231245:R>, emoji <a:emoji_132.abc:321> <:emoji:321>, remove mentions <@!12345> <@3214512> <@&12345> <#32134>
        self.message = re.sub(r'<[#@:ta][&!]?[^>]+R?>', '', self.message).strip()
    
    def _remove_links(self) -> None:
        self.message = re.sub(r'https?://[^\s]+', '', self.message)
        
    def _expand_abbreviations(self) -> None:
        if 'abbreviations' not in self.config:
            return
        for abbreviation, expansion in self.config['abbreviations'].items():
            self.message = self.message.replace(abbreviation, expansion)
    
    def _is_reply_to(self, line: str) -> None:
        return line.startswith('-# Reply to')
        
    def _is_delay_note(self, line: str) -> None:
        return line.startswith('-# :small_blue_diamond: Posted at')
    
    
class TranslationHistory:
    max_history_size = 50
    
    def __init__(self):
        self.history = {}
        
    def _get_hash(self, message: str) -> str:
        return hashlib.sha256(message.encode()).hexdigest()
    
    def add_message(self, message: str, translation: str) -> None:
        self.history[self._get_hash(message)] = translation
        if len(self.history) > self.max_history_size:
            self.history.pop(next(iter(self.history)))
    
    def find_translation(self, message: str) -> str:
        return self.history.get(self._get_hash(message), None)


class Dranslator(discord.Client):
    def __init__(self, config_file: str):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        
        self.error_report_channel = None
        self.cached_channels: dict[int, discord.TextChannel] = {}
        self.translated_message_ids: list[int] = []
        self.load_config(config_file)
        
        self.translation_history = TranslationHistory()
        
    def run_bot(self, token: str = DISCORD_BOT_TOKEN):
        self.run(token, log_handler=stream_handler)
        
    def get_cached_channel(self, channel_id: int) -> discord.TextChannel:
        if channel_id not in self.cached_channels:
            self.cached_channels[channel_id] = self.get_channel(channel_id)
        return self.cached_channels[channel_id]

    async def on_ready(self):
        logger.info(f'Translator logged on as {self.user}')
        self.cache_channels()
        
    def cache_channels(self):
        logger.info(f"Caching channels for auto message translation...")
        for channel_id in self.config['channels']:
            channel = self.get_cached_channel(channel_id)
            if channel is None:
                logger.error(f"Channel {channel_id} not found.")
                continue
            logger.info(f"Channel {channel.guild.name}/{channel.name} added.")
        
        if channel := self.config.get('error_report_channel', None):
            self.error_report_channel = self.get_cached_channel(channel)
            
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.user_id == self.user.id:
            return
        
        if payload.emoji.name != TRIGGER_EMOJI:
            return
        
        message = await self.get_channel(payload.channel_id).fetch_message(payload.message_id)
        for reaction in message.reactions:
            if reaction.emoji == TRIGGER_EMOJI and reaction.count >= 2:
                # already translated
                return
        await self._translate_and_send_message(message)
    
    async def on_message(self, message: discord.Message):
        if message.channel.id not in self.config['channels'] or message.author.id == self.user.id:
            return
        await self._translate_and_send_message(message)
    
    async def _translate_and_send_message(self, discord_message: discord.Message) -> None:
        content = MessagePreProcessor(discord_message.content, self.config).preprocess()
        if not self._is_translation_required(content):
            return
        success,content = self._get_translation(content)
        if not success:
            if self.error_report_channel:
                await self._report_error(discord_message, content)
                return
        channel = self.get_cached_channel(discord_message.channel.id)
        message = await channel.send(content = content, 
                           reference = discord_message)
        if message and message.id > 0:
            self.translated_message_ids.append(message.id)
    
    def _is_translation_required(self, message: str) -> bool:
        if message == '':
            logger.info(f"Empty message... Skipping.")
            return False
        if is_mostly_chinese(message):
            logger.info(f"Appears to be a Chinese message... Skipping.")
            return False
        if is_ticker_only(message):
            logger.info(f"Appears to be a ticker only message... Skipping.")
            return False
        if is_punctuation_only(message):
            logger.info(f"Appears to be a punctuation only message... Skipping.")
            return False
        return True
    
    def _get_translation(self, message: str) -> (bool, str):
        translation = self.translation_history.find_translation(message)
        if translation:
            logger.info(f"Translation found in history.")
            return (True, translation)
        
        response = translate(message)
        
        error_text = response.get('error', None)
        if response is None or error_text:
            logger.error(f"Error translating message: {message}. \n{error_text}")
            return (False, f'-# :small_orange_diamond:Translation failed\n{error_text}')
        
        translation = response['translation']
        self.translation_history.add_message(message, translation)
        return (True, translation)
    
    async def _report_error(self, discord_message: discord.Message, error_text: str) -> None:
        if self.error_report_channel:
            content = f"{error_text} | {discord_message.jump_url}"
            await self.error_report_channel.send(content)

    
    def load_config(self, config_file: str):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
