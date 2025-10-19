"""
==============================================================================
Project: GuajiraSustainableWindBot
File: supervisor_code_agent_test.py
Description:
    Interactive console interface for the text-to-python multi-agent system.
    This script provides a user-friendly CLI to interact with the code agents.

Usage:
    python supervisor_code_agent_test.py

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
import traceback
import matplotlib
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

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

# Check API key
if not os.getenv("OPENAI_API_KEY"):
    print(f"{Fore.RED}❌ Error: OPENAI_API_KEY not found in .env file{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Please add your OpenAI API key to .env{Style.RESET_ALL}")
    sys.exit(1)

# Import the multi-agent system
try:
    from src.code_agent import CodeMultiAgentSystem
except ImportError as e:
    print(f"{Fore.RED}❌ Error importing CodeMultiAgentSystem: {e}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Make sure you're in the project root directory{Style.RESET_ALL}")
    sys.exit(1)

# ==============================================================================================
# Main Interactive Loop
# ==============================================================================================

def run_code_multiagent_chatbot():
    """Main chat loop with code-enabled multi-agent system."""
    print(f"\n{Fore.CYAN}{'='*80}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🌬️  WindBot Multi-Agent System (Text-to-Python){Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Análisis Preciso de Viento con Generación de Código{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}📋 Sistema: 1 Supervisor + 13 Agentes con Python + 1 Agente General{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🐍 Capacidad: Generación y ejecución de código Python para análisis{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 Ventaja: Cero alucinaciones en datos numéricos{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🚪 Escribe 'exit' para salir{Style.RESET_ALL}\n")
    
    # Initialize multi-agent system
    try:
        system = CodeMultiAgentSystem(verbose=True)
    except Exception as e:
        print(f"{Fore.RED}❌ Error inicializando sistema: {e}{Style.RESET_ALL}")
        print(traceback.format_exc())
        sys.exit(1)
    
    try:
        while True:
            user_input = input(f"{Fore.GREEN}👤 Tú: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "salir"]:
                print(f"\n{Fore.MAGENTA}👋 Hasta pronto! Sistema desconectado.{Style.RESET_ALL}\n")
                break
            
            try:
                print(f"\n{Fore.CYAN}{'─'*80}{Style.RESET_ALL}\n")
                response = system.process_query(user_input, verbose=True)
                print(f"\n{Fore.CYAN}{'─'*80}{Style.RESET_ALL}")
                print(f"{Fore.BLUE}🤖 Bot:{Style.RESET_ALL}\n{response}\n")
                print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}\n")
                print(f"{Fore.RED}{traceback.format_exc()}{Style.RESET_ALL}\n")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Chat finalizado{Style.RESET_ALL}\n")


# ==============================================================================================
# Entry Point
# ==============================================================================================

if __name__ == "__main__":
    run_code_multiagent_chatbot()
