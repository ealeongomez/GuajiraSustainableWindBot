"""
==============================================================================
Project: GuajiraSustainableWindBot
File: telegram_chatbot.py
Description:
    Telegram-based chatbot for wind speed forecasting in La Guajira.
    This script implements a conversational LLM with user-specific memory,
    identified uniquely by Telegram user ID, to handle context about
    wind predictions and sustainable energy.

Author: Eder Arley León Gómez
Created on: 2025-10-18
==============================================================================
"""

import sys
import warnings
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import bot configuration and handlers
from src.telegram_bot.config import TELEGRAM_BOT_TOKEN
from src.telegram_bot.handlers import (
    start_command,
    help_command,
    clear_command,
    handle_message,
    error_handler
)

# Disable warnings
warnings.filterwarnings("ignore")

def main():
    """Start the Telegram bot"""
    print("✅ Modelo OpenAI inicializado: GPT-3.5-turbo")
    print("✅ Prompt template cargado\n")
    print("🤖 Iniciando WindBot para Telegram...")
    print(f"🔑 Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    print("✅ Bot listo. Esperando mensajes...\n")

    # Build the Telegram application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("clear", clear_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Add error handler
    application.add_error_handler(error_handler)

    # Run bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
