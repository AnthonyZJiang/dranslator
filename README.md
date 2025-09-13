# VF Translator (Dranslator)

A Discord bot that automatically translates messages in specified channels. Supports abbreviation expansion, intelligent message filtering, and translation history caching.

## Features

- **Real-time Translation**: Automatically translates messages as they appear in configured channels
- **Reaction-based Triggering**: Translate messages on-demand using emoji reactions
- **Abbreviation Expansion**: Automatically expands custom abbreviations (e.g., "HVE" → "Highest Volume Ever")
- **Intelligent Filtering**: Skips messages that are:
  - Mostly Chinese text
  - Ticker symbols only
  - Punctuation only
  - Empty or irrelevant content
- **Translation Caching**: Stores recent translations to avoid duplicate API calls
- **Multiple Translator Support**: Supports Azure Translator, DeepL, Gemini, and OpenAI for high-quality translations
- **Message Preprocessing**: Removes Discord formatting, links, and other noise before translation

## Prerequisites

- Python 3.8+
- Discord Bot Token
- Translation service API key (Azure Translator, DeepL, Gemini, or OpenAI)
- Discord server with appropriate permissions

## Installation

1. **Clone or navigate to the project:**
```bash
cd vftranslator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
Create a `.env` file in the project root:
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
TRIGGER_EMOJI=🔤
TRANSLATOR=azure
```

4. **Configure the bot:**
Edit `config.json` to specify target channels and abbreviations:
```json
{
    "channels": [1395334506176577677, 1395385591981412453],
    "abbreviations": {
        "HVE": "Highest Volume Ever",
        "ATH": "All Time High",
        "ATL": "All Time Low",
        "KMS": "Key Moving Average"
    }
}
```

## Configuration

### Environment Variables (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `DISCORD_BOT_TOKEN` | Your Discord bot token | Yes |
| `TRIGGER_EMOJI` | Emoji to trigger manual translations | Yes |
| `TRANSLATOR` | Translation service to use (`azure`, `deepl`, `gemini`, `openai`) | Yes |
| `TRANSLATE_FROM_LANGUAGE` | Source language code (e.g., `en`, `zh`) | Yes |
| `TRANSLATE_TO_LANGUAGE` | Target language code (e.g., `zh`, `en`) | Yes |

#### Azure Translator Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_TRANSLATOR_KEY` | Your Azure Translator API key | Yes (if using Azure) |
| `AZURE_TRANSLATOR_REGION` | Your Azure Translator region | Yes (if using Azure) |

#### DeepL Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `DEEPL_API_KEY` | Your DeepL API key | Yes (if using DeepL) |
| `DEEPL_GLOSSARY_ID` | Optional DeepL glossary ID for custom terminology | No |

#### Gemini Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Your Google Gemini API key | Yes (if using Gemini) |

#### OpenAI Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | Yes (if using OpenAI) |
| `PROMPT_ID` | OpenAI prompt ID for translation | Yes (if using OpenAI) |

### Configuration File (config.json)

| Field | Type | Description |
|-------|------|-------------|
| `channels` | Array of integers | Discord channel IDs to monitor |
| `abbreviations` | Object | Key-value pairs for abbreviation expansion |

## Usage

### Starting the Bot

```bash
python run_translator.py
```

### How It Works

1. **Automatic Translation**: The bot monitors specified channels and automatically translates new messages
2. **Reaction Triggering**: Users can add the configured emoji reaction to any message to trigger translation
3. **Translation History**: Previously translated messages are cached to avoid duplicate API calls
4. **Message Preprocessing**: Messages are cleaned of Discord formatting, links, and other noise before translation

### Translation Process

1. **Message Filtering**: Checks if translation is needed (skips Chinese, tickers, etc.)
2. **Preprocessing**: Removes Discord formatting, links, and expands abbreviations
3. **Translation**: Sends to Azure Translator API
4. **Caching**: Stores translation in memory for future use
5. **Posting**: Sends translated message as a reply to the original

## Message Filtering

The bot intelligently filters messages to avoid unnecessary translations:

- **Chinese Text**: Skips messages that are mostly Chinese characters
- **Ticker Symbols**: Skips messages containing only stock tickers
- **Punctuation Only**: Skips messages with only punctuation marks
- **Empty Content**: Skips empty or whitespace-only messages
- **Discord Commands**: Automatically removes Discord formatting and commands

## Abbreviation Expansion

Configure custom abbreviations in `config.json`:

```json
{
    "abbreviations": {
        "HVE": "Highest Volume Ever",
        "ATH": "All Time High",
        "ATL": "All Time Low",
        "KMS": "Key Moving Average",
        "RSI": "Relative Strength Index",
        "MACD": "Moving Average Convergence Divergence"
    }
}
```

## Translator Service Setup

Choose one of the following translation services and follow the setup instructions:

### Azure Translator Setup

1. **Get Azure Translator Key:**
   - Sign up for [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/)
   - Create a Translator resource
   - Copy your API key and region

2. **Configure Environment:**
   Add these variables to your `.env` file:
   ```env
   TRANSLATOR=azure
   AZURE_TRANSLATOR_KEY=your_azure_key_here
   AZURE_TRANSLATOR_REGION=your_azure_region_here
   TRANSLATE_FROM_LANGUAGE=en
   TRANSLATE_TO_LANGUAGE=zh
   ```

### DeepL Setup

1. **Get DeepL API Key:**
   - Sign up for [DeepL API](https://www.deepl.com/pro-api)
   - Create an API key from your account dashboard
   - Optionally create a glossary for custom terminology

2. **Configure Environment:**
   Add these variables to your `.env` file:
   ```env
   TRANSLATOR=deepl
   DEEPL_API_KEY=your_deepl_key_here
   DEEPL_GLOSSARY_ID=your_glossary_id_here  # Optional
   TRANSLATE_FROM_LANGUAGE=EN
   TRANSLATE_TO_LANGUAGE=ZH
   ```

### Gemini Setup

1. **Get Gemini API Key:**
   - Go to [Google AI Studio](https://aistudio.google.com/)
   - Create an API key
   - Enable the Gemini API

2. **Configure Environment:**
   Add these variables to your `.env` file:
   ```env
   TRANSLATOR=gemini
   GEMINI_API_KEY=your_gemini_key_here
   TRANSLATE_FROM_LANGUAGE=en
   TRANSLATE_TO_LANGUAGE=zh
   ```

### OpenAI Setup

1. **Get OpenAI API Key:**
   - Sign up for [OpenAI API](https://platform.openai.com/)
   - Create an API key
   - Set up a custom prompt for translation

2. **Configure Environment:**
   Add these variables to your `.env` file:
   ```env
   TRANSLATOR=openai
   OPENAI_API_KEY=your_openai_key_here
   PROMPT_ID=your_prompt_id_here
   TRANSLATE_FROM_LANGUAGE=en
   TRANSLATE_TO_LANGUAGE=zh
   ```

## Translator Comparison

| Feature | Azure | DeepL | Gemini | OpenAI |
|---------|-------|-------|--------|--------|
| **Quality** | High | Very High | High | Very High |
| **Speed** | Fast | Fast | Medium | Medium |
| **Cost** | Pay-per-use | Pay-per-use | Pay-per-use | Pay-per-use |
| **Languages** | 100+ | 30+ | 100+ | 100+ |
| **Custom Terminology** | Yes | Yes (Glossaries) | No | Yes (Prompts) |
| **Rate Limits** | High | Medium | Medium | High |
| **Specialization** | General | European languages | General | General |

## Discord Bot Setup

1. **Create a Discord Application:**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Go to the "Bot" section and create a bot

2. **Configure Bot Permissions:**
   - Read Messages
   - Send Messages
   - Add Reactions
   - Read Message History
   - Use External Emojis

3. **Invite Bot to Server:**
   - Use the OAuth2 URL generator
   - Select the required scopes and permissions
   - Invite the bot to your server

## Project Structure

```
vftranslator/
├── dranslator/
│   ├── __init__.py
│   ├── dranslator.py          # Main bot implementation
│   ├── util.py               # Utility functions
│   └── translator/
│       ├── __init__.py
│       ├── azuretranslator.py # Azure Translator integration
│       ├── deepltranslator.py # DeepL Translator integration
│       ├── geminitranslator.py # Gemini Translator integration
│       └── openaitranslator.py # OpenAI Translator integration
├── config.json               # Bot configuration
├── run_translator.py         # Entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Dependencies

### Core Dependencies
- `discord.py` - Discord bot framework
- `python-dotenv` - Environment variable management
- `hashlib` - Message hashing for caching

### Translator-Specific Dependencies
- `azure-ai-translation-text` - Azure Translator integration
- `deepl` - DeepL API integration
- `google-genai` - Gemini API integration
- `openai` - OpenAI API integration
- `tiktoken` - Token counting for OpenAI

## Error Handling

The bot includes comprehensive error handling:

- **API Failures**: Gracefully handles translation API errors
- **Network Issues**: Continues operation during temporary network problems
- **Invalid Messages**: Skips messages that can't be processed
- **Rate Limiting**: Respects Discord and Azure API rate limits

## Contributing

Contributions are welcome! Please feel free to submit Pull Requests for:

- New translation providers
- Additional message filtering options
- Performance improvements
- Bug fixes

## License

MIT License

## Support

If you encounter issues:

1. Check your configuration files
2. Verify your Discord bot permissions
3. Ensure your Azure Translator API key is valid
4. Check the bot logs for error messages

## Troubleshooting

### Common Issues

**Bot not responding:**
- Verify the bot token is correct
- Check that the bot has proper permissions
- Ensure the bot is online in Discord

**Translations not working:**
- Verify your chosen translator API key and configuration
- Check network connectivity
- Review the bot logs for API errors
- Ensure the `TRANSLATOR` environment variable is set correctly
- For Azure: Verify region and key are correct
- For DeepL: Check API key and language codes (use uppercase)
- For Gemini: Ensure API key is valid and Gemini API is enabled
- For OpenAI: Verify API key and prompt ID are correct

**Messages not being translated:**
- Verify channel IDs in config.json
- Check if messages are being filtered out
- Ensure the bot has access to the channels
