"""
Configuration for Code Agent System
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
MODELS_DIR = PROJECT_ROOT / "models" / "LSTM"
OUTPUT_DIR = PROJECT_ROOT / "test" / "chatbot" / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Load environment variables
env_path = PROJECT_ROOT / '.env'
load_dotenv(dotenv_path=env_path)

# Municipalities
MUNICIPALITIES = [
    "albania", "barrancas", "distraccion", "el_molino", "fonseca", 
    "hatonuevo", "la_jagua_del_pilar", "maicao", "manaure", "mingueo", 
    "riohacha", "san_juan_del_cesar", "uribia"
]

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM models
def get_supervisor_llm():
    """Get supervisor LLM instance."""
    return ChatOpenAI(
        model="gpt-4",
        temperature=0.1,
        max_retries=2,
        api_key=OPENAI_API_KEY
    )

def get_agent_llm():
    """Get agent LLM instance."""
    return ChatOpenAI(
        model="gpt-4",
        temperature=0,
        max_retries=2,
        api_key=OPENAI_API_KEY
    )

