"""
==============================================================================
Project: GuajiraSustainableWindBot
File: console_chatbot_test.py
Description:
    Console-based chatbot for wind speed forecasting in La Guajira.
    This script implements a conversational LLM with short-term memory
    to handle context about wind predictions and sustainable energy.

Author: Eder Arley León Gómez
Created on: 2025-10-18
==============================================================================
"""

# ==============================================================================================
# Libraries 
# ==============================================================================================

# Basics
import os
import sys
import warnings
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

# LangChain core
from langchain_openai import ChatOpenAI                  # OpenAI API
from langchain.chains import LLMChain                    # Chain with prompt
from langchain_core.prompts import PromptTemplate        # Prompt design
from langchain.memory import ConversationBufferMemory    # Conversational memory

# Initialize colorama
init(autoreset=True)

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import prompt loader
from src.prompt_template import load_prompt

# Disable warnings
warnings.filterwarnings("ignore")

# Load environment variables from project root
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# ==============================================================================================
# Variables and Configuration
# ==============================================================================================

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI LLM
LLM = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    max_retries=2,
    api_key=OPENAI_API_KEY
)
print(f"{Fore.GREEN}✅ Usando modelo: OpenAI GPT-3.5-turbo{Style.RESET_ALL}\n")

# Memory for conversation
memory = ConversationBufferMemory(input_key="pregunta", memory_key="history")

# ==============================================================================================
# Prompt Definition
# ==============================================================================================

# Load prompt template from external file
prompt_template = load_prompt("windbot_prompt")
    

prompt = PromptTemplate(
    input_variables=["pregunta", "history"],
    template=prompt_template
)

# Create the LLM chain
llm_chain = LLMChain(
    prompt=prompt,
    llm=LLM,
    memory=memory
)

# ==============================================================================================
# Interaction Loop
# ==============================================================================================

def run_chatbot():
    """Main chat loop."""
    print(f"\n{Fore.CYAN}🌬️  WindBot - Predicción de Viento en La Guajira{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Escribe 'exit' para salir{Style.RESET_ALL}\n")
    
    try:
        while True:
            user_input = input(f"{Fore.GREEN} 👤 Tú: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "salir"]:
                print(f"\n{Fore.MAGENTA}👋 Hasta pronto!{Style.RESET_ALL}\n")
                break
            
            try:
                response = llm_chain.invoke({"pregunta": user_input})
                print(f"{Fore.BLUE}🤖 Bot: {Style.RESET_ALL}{response['text']}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}\n")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Chat finalizado{Style.RESET_ALL}\n")

# ==============================================================================================
# Entry Point
# ==============================================================================================

if __name__ == "__main__":
    run_chatbot()
