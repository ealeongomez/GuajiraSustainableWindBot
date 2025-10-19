"""
==============================================================================
Project: GuajiraSustainableWindBot
File: supervisor_multiagent_test.py
Description:
    Multi-agent system with supervisor and municipality-specific sub-agents.
    The supervisor routes queries to specialized agents for each municipality.
    Each sub-agent has access to specific data and expertise about its municipality.

Author: Eder Arley León Gómez
Created on: 2025-10-19
==============================================================================
"""

# ==============================================================================================
# Libraries 
# ==============================================================================================

# Basics
import os
import sys
import warnings
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from colorama import Fore, Style, init
from typing import Dict, List, Optional

# LangChain core
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Initialize colorama
init(autoreset=True)

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Disable warnings
warnings.filterwarnings("ignore")

# Load environment variables from project root
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

# ==============================================================================================
# Configuration
# ==============================================================================================

# Municipalities available
MUNICIPALITIES = [
    "albania", "barrancas", "distraccion", "el_molino", "fonseca", 
    "hatonuevo", "la_jagua_del_pilar", "maicao", "manaure", "mingueo", 
    "riohacha", "san_juan_del_cesar", "uribia"
]

# Paths
DATA_DIR = project_root / "data" / "raw"
MODELS_DIR = project_root / "models" / "LSTM"

# Get OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize LLM models
supervisor_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.1,
    max_retries=2,
    api_key=OPENAI_API_KEY
)

subagent_llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    max_retries=2,
    api_key=OPENAI_API_KEY
)

print(f"{Fore.GREEN}✅ Modelos LLM inicializados correctamente{Style.RESET_ALL}\n")

# ==============================================================================================
# Data Loading Functions
# ==============================================================================================

def load_municipality_data(municipality: str) -> Optional[pd.DataFrame]:
    """
    Load data for a specific municipality.
    
    Args:
        municipality: Name of the municipality
        
    Returns:
        DataFrame with municipality data or None if not found
    """
    try:
        csv_file = DATA_DIR / f"open_meteo_{municipality}.csv"
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            return df
        else:
            return None
    except Exception as e:
        print(f"{Fore.RED}Error loading data for {municipality}: {e}{Style.RESET_ALL}")
        return None


def get_municipality_stats(municipality: str) -> Dict:
    """
    Get statistical summary for a municipality.
    
    Args:
        municipality: Name of the municipality
        
    Returns:
        Dictionary with statistics
    """
    df = load_municipality_data(municipality)
    if df is None:
        return {}
    
    stats = {
        "municipality": municipality,
        "records": len(df),
        "wind_speed_avg": round(df['wind_speed_10m'].mean(), 2),
        "wind_speed_max": round(df['wind_speed_10m'].max(), 2),
        "wind_speed_min": round(df['wind_speed_10m'].min(), 2),
        "temperature_avg": round(df['temperature_2m'].mean(), 2),
        "humidity_avg": round(df['relative_humidity_2m'].mean(), 2),
        "date_range": f"{df['datetime'].min()} a {df['datetime'].max()}"
    }
    
    return stats


# ==============================================================================================
# Supervisor Agent
# ==============================================================================================

class SupervisorAgent:
    """
    Supervisor agent that routes queries to municipality-specific sub-agents.
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.memory = ConversationBufferMemory(
            memory_key="history", 
            return_messages=True
        )
        
        # Supervisor prompt
        self.prompt = ChatPromptTemplate.from_template(
            """Eres un agente supervisor de WindBot, un sistema experto en predicción de viento 
en La Guajira, Colombia.

Tu tarea es analizar la consulta del usuario e identificar:
1. ¿De qué municipio(s) está preguntando el usuario?
2. ¿Es una pregunta general o específica de un municipio?

Los 13 municipios disponibles son:
Albania, Barrancas, Distracción, El Molino, Fonseca, Hatonuevo, La Jagua del Pilar,
Maicao, Manaure, Mingueo, Riohacha, San Juan del Cesar, Uribia.

Responde ÚNICAMENTE con uno de estos formatos:
- Si es específico de un municipio: "MUNICIPIO: [nombre_del_municipio]"
- Si es general: "GENERAL"
- Si menciona varios municipios: "MUNICIPIOS: [municipio1, municipio2, ...]"

Consulta del usuario: {query}

Análisis:"""
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def route_query(self, query: str) -> Dict:
        """
        Route the query to appropriate sub-agent(s).
        
        Args:
            query: User's question
            
        Returns:
            Dictionary with routing information
        """
        try:
            response = self.chain.invoke({"query": query})
            
            # Parse response
            if response.startswith("MUNICIPIO:"):
                municipality = response.split(":", 1)[1].strip().lower()
                # Normalize municipality name
                municipality = municipality.replace(" ", "_").replace("á", "a").replace("ó", "o")
                return {
                    "type": "specific",
                    "municipalities": [municipality]
                }
            elif response.startswith("MUNICIPIOS:"):
                municipalities_str = response.split(":", 1)[1].strip()
                municipalities = [
                    m.strip().lower().replace(" ", "_").replace("á", "a").replace("ó", "o")
                    for m in municipalities_str.split(",")
                ]
                return {
                    "type": "multiple",
                    "municipalities": municipalities
                }
            else:
                return {
                    "type": "general",
                    "municipalities": []
                }
        except Exception as e:
            print(f"{Fore.RED}Error en supervisor: {e}{Style.RESET_ALL}")
            return {
                "type": "general",
                "municipalities": []
            }


# ==============================================================================================
# Sub-Agent (Municipality Specific)
# ==============================================================================================

class MunicipalityAgent:
    """
    Specialized agent for a specific municipality.
    """
    
    def __init__(self, municipality: str, llm):
        self.municipality = municipality
        self.llm = llm
        self.stats = get_municipality_stats(municipality)
        
        # Sub-agent prompt
        self.prompt = ChatPromptTemplate.from_template(
            """Eres un agente experto en predicción de viento para el municipio de {municipality_display}.

Información disponible del municipio:
- Registros totales: {records}
- Velocidad del viento promedio: {wind_speed_avg} m/s
- Velocidad del viento máxima: {wind_speed_max} m/s
- Velocidad del viento mínima: {wind_speed_min} m/s
- Temperatura promedio: {temperature_avg} °C
- Humedad relativa promedio: {humidity_avg}%
- Rango de fechas: {date_range}

Tu tarea es responder preguntas específicas sobre {municipality_display} usando esta información.
Proporciona respuestas precisas, técnicas pero comprensibles.

Pregunta del usuario: {query}

Respuesta (como experto en {municipality_display}):"""
        )
    
    def answer(self, query: str) -> str:
        """
        Answer query about this municipality.
        
        Args:
            query: User's question
            
        Returns:
            Response string
        """
        try:
            if not self.stats:
                return f"No tengo datos disponibles para {self.municipality}."
            
            municipality_display = self.municipality.replace("_", " ").title()
            
            chain = self.prompt | self.llm | StrOutputParser()
            
            response = chain.invoke({
                "municipality_display": municipality_display,
                "query": query,
                **self.stats
            })
            
            return response
            
        except Exception as e:
            return f"Error al procesar consulta: {e}"


# ==============================================================================================
# General Agent
# ==============================================================================================

class GeneralAgent:
    """
    General agent for non-municipality-specific queries.
    """
    
    def __init__(self, llm):
        self.llm = llm
        
        self.prompt = ChatPromptTemplate.from_template(
            """Eres WindBot, un asistente experto en predicción de viento y energía sostenible 
en La Guajira, Colombia.

Monitoras 13 municipios: Albania, Barrancas, Distracción, El Molino, Fonseca, Hatonuevo, 
La Jagua del Pilar, Maicao, Manaure, Mingueo, Riohacha, San Juan del Cesar y Uribia.

Tu tarea es responder preguntas generales sobre:
- Energía eólica y sostenibilidad
- Modelos de predicción LSTM
- Información general sobre La Guajira
- Conceptos técnicos sobre viento y meteorología

Responde ÚNICAMENTE en español de forma clara y técnica.

Pregunta del usuario: {query}

Respuesta:"""
        )
    
    def answer(self, query: str) -> str:
        """
        Answer general query.
        
        Args:
            query: User's question
            
        Returns:
            Response string
        """
        try:
            chain = self.prompt | self.llm | StrOutputParser()
            response = chain.invoke({"query": query})
            return response
        except Exception as e:
            return f"Error al procesar consulta: {e}"


# ==============================================================================================
# Multi-Agent System Orchestrator
# ==============================================================================================

class MultiAgentSystem:
    """
    Orchestrates the supervisor and sub-agents.
    """
    
    def __init__(self):
        self.supervisor = SupervisorAgent(supervisor_llm)
        self.general_agent = GeneralAgent(subagent_llm)
        self.municipality_agents: Dict[str, MunicipalityAgent] = {}
        
        # Initialize municipality agents
        for municipality in MUNICIPALITIES:
            self.municipality_agents[municipality] = MunicipalityAgent(
                municipality, 
                subagent_llm
            )
        
        print(f"{Fore.GREEN}✅ Sistema multi-agente inicializado con {len(MUNICIPALITIES)} agentes municipales{Style.RESET_ALL}\n")
    
    def process_query(self, query: str) -> str:
        """
        Process user query through the multi-agent system.
        
        Args:
            query: User's question
            
        Returns:
            Final response
        """
        # Step 1: Supervisor routes the query
        print(f"{Fore.YELLOW}🔍 Supervisor analizando consulta...{Style.RESET_ALL}")
        routing = self.supervisor.route_query(query)
        
        # Step 2: Based on routing, delegate to appropriate agent(s)
        if routing["type"] == "specific":
            municipality = routing["municipalities"][0]
            print(f"{Fore.CYAN}📍 Enrutando a agente de {municipality.replace('_', ' ').title()}{Style.RESET_ALL}")
            
            if municipality in self.municipality_agents:
                return self.municipality_agents[municipality].answer(query)
            else:
                return f"Municipio '{municipality}' no encontrado en el sistema."
        
        elif routing["type"] == "multiple":
            print(f"{Fore.CYAN}📍 Consultando múltiples municipios{Style.RESET_ALL}")
            responses = []
            for municipality in routing["municipalities"]:
                if municipality in self.municipality_agents:
                    response = self.municipality_agents[municipality].answer(query)
                    responses.append(f"\n**{municipality.replace('_', ' ').title()}:**\n{response}")
            return "\n".join(responses) if responses else "No se encontraron municipios válidos."
        
        else:  # general
            print(f"{Fore.CYAN}🌐 Respondiendo con agente general{Style.RESET_ALL}")
            return self.general_agent.answer(query)


# ==============================================================================================
# Interaction Loop
# ==============================================================================================

def run_multiagent_chatbot():
    """Main chat loop with multi-agent system."""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}🌬️  WindBot Multi-Agent System{Style.RESET_ALL}")
    print(f"{Fore.CYAN}    Predicción de Viento en La Guajira{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}📋 Sistema: 1 Supervisor + 13 Agentes Municipales + 1 Agente General{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}💡 Tip: Pregunta sobre municipios específicos o temas generales{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}🚪 Escribe 'exit' para salir{Style.RESET_ALL}\n")
    
    # Initialize multi-agent system
    system = MultiAgentSystem()
    
    try:
        while True:
            user_input = input(f"{Fore.GREEN}👤 Tú: {Style.RESET_ALL}").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "salir"]:
                print(f"\n{Fore.MAGENTA}👋 Hasta pronto! Sistema multi-agente desconectado.{Style.RESET_ALL}\n")
                break
            
            try:
                print()  # Line break
                response = system.process_query(user_input)
                print(f"\n{Fore.BLUE}🤖 Bot: {Style.RESET_ALL}{response}\n")
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}\n")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.MAGENTA}Chat finalizado{Style.RESET_ALL}\n")


# ==============================================================================================
# Entry Point
# ==============================================================================================

if __name__ == "__main__":
    run_multiagent_chatbot()

