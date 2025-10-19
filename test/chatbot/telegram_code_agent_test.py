"""
==============================================================================
Project: GuajiraSustainableWindBot
File: telegram_code_agent_test.py
Description:
    Telegram bot interface for the text-to-python multi-agent system.
    This script provides a Telegram frontend to interact with the 
    CodeMultiAgentSystem for wind data analysis in La Guajira.

Features:
    - Multi-agent system with code generation capabilities
    - Zero-hallucination data analysis using Python code execution
    - User-specific conversation history via MongoDB
    - LangSmith tracing for monitoring and debugging
    - Secure code execution environment

Usage:
    python telegram_code_agent_test.py

Requirements:
    - TELEGRAM_BOT_TOKEN in .env
    - OPENAI_API_KEY in .env
    - MONGODB_URI in .env (optional, for conversation storage)
    - LANGCHAIN_API_KEY in .env (optional, for tracing)

Author: Eder Arley León Gómez
Created on: 2025-10-19
==============================================================================
"""

# ==============================================================================================
# Libraries 
# ==============================================================================================

import os
import sys
import warnings
import matplotlib
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Configure matplotlib for non-interactive backend
matplotlib.use('Agg')

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Disable warnings
warnings.filterwarnings("ignore")

# Load environment variables
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# Import Telegram configuration and code agent handlers
from src.telegram_bot.config import TELEGRAM_BOT_TOKEN
from src.telegram_bot.code_agent_handlers import (
    start_command_code,
    help_command_code,
    clear_command_code,
    handle_message_code,
    error_handler_code
)

# ==============================================================================================
# Validation
# ==============================================================================================

# Check required API keys
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: OPENAI_API_KEY not found in .env file")
    print("⚠️  Please add your OpenAI API key to .env")
    sys.exit(1)

if not TELEGRAM_BOT_TOKEN:
    print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
    print("⚠️  Please add your Telegram bot token to .env")
    sys.exit(1)

# ==============================================================================================
# Main Function
# ==============================================================================================

def main():
    """Start the Telegram bot with CodeMultiAgentSystem"""
    print("\n" + "="*80)
    print("🌬️  WindBot Code Agent - Telegram Interface")
    print("    Análisis Preciso de Viento con Text-to-Python Multi-Agent System")
    print("="*80 + "\n")
    
    print("📋 Sistema: 1 Supervisor + 13 Agentes Municipales + 1 Agente General")
    print("🐍 Capacidad: Generación y ejecución de código Python para análisis")
    print("💡 Ventaja: Cero alucinaciones en datos numéricos")
    print("📊 Output: Gráficos guardados en test/chatbot/output/")
    print(f"🔑 Token: {TELEGRAM_BOT_TOKEN[:10]}...")
    
    # Check optional services
    if os.getenv("MONGODB_URI"):
        print("✅ MongoDB conectado para almacenamiento de conversaciones")
    else:
        print("⚠️  MongoDB no configurado (conversaciones no se guardarán)")
    
    if os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true":
        print("✅ LangSmith tracing habilitado")
    else:
        print("ℹ️  LangSmith tracing no habilitado")
    
    print("\n🤖 Iniciando bot de Telegram...")
    print("✅ Bot listo. Esperando mensajes...\n")
    print("="*80 + "\n")

    # Build the Telegram application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register handlers for code agent system
    application.add_handler(CommandHandler("start", start_command_code))
    application.add_handler(CommandHandler("help", help_command_code))
    application.add_handler(CommandHandler("clear", clear_command_code))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message_code))

    # Add error handler
    application.add_error_handler(error_handler_code)

    # Run bot
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n\n🛑 Bot detenido por el usuario")
        print("👋 Hasta pronto!\n")
    except Exception as e:
        print(f"\n❌ Error fatal: {e}\n")
        sys.exit(1)


# ==============================================================================================
# Entry Point
# ==============================================================================================

if __name__ == "__main__":
    main()

