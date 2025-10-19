"""
Configuration for Telegram Bot
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# Import prompt loader
from src.prompt_template import load_prompt

# Get API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# LangSmith configuration (using LANGCHAIN_ prefix from .env)
LANGSMITH_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

# Configure LangSmith if enabled
if LANGSMITH_TRACING and LANGSMITH_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
    os.environ["LANGCHAIN_API_KEY"] = LANGSMITH_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "GuajiraSustainableWindBot-Telegram")
    print("✅ LangSmith tracing habilitado")

# Validate API keys
if not TELEGRAM_BOT_TOKEN:
    print("❌ ERROR: TELEGRAM_BOT_TOKEN no encontrado en .env")
    sys.exit(1)

if not OPENAI_API_KEY:
    print("❌ ERROR: OPENAI_API_KEY no encontrado en .env")
    sys.exit(1)

# Initialize OpenAI model
LLM = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    max_retries=2,
    api_key=OPENAI_API_KEY
)

# Load prompt template
prompt_template = load_prompt("windbot_prompt")

# Create prompt
PROMPT = PromptTemplate(
    input_variables=["pregunta", "history"],
    template=prompt_template
)

# Dictionary to store user-specific memories (in-memory cache)
# Histories are loaded from MongoDB on first access
USER_MEMORIES = {}

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")

