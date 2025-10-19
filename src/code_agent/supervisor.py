"""
Supervisor Agent - Routes queries to appropriate agents
"""

from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from colorama import Fore, Style


class SupervisorAgent:
    """Supervisor agent that routes queries and determines if code execution is needed."""
    
    def __init__(self, llm):
        """
        Initialize Supervisor Agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
        
        # Supervisor prompt
        self.prompt = ChatPromptTemplate.from_template(
            """Eres un agente supervisor de WindBot, especializado EXCLUSIVAMENTE en enrutar consultas sobre viento en La Guajira, Colombia.

IMPORTANTE: Solo procesas consultas relacionadas con:
- Predicción y análisis de viento
- Energía eólica y sostenibilidad
- Los 13 municipios de La Guajira: Albania, Barrancas, Distracción, El Molino, Fonseca, Hatonuevo, La Jagua del Pilar, Maicao, Manaure, Mingueo, Riohacha, San Juan del Cesar, Uribia

Tu tarea es analizar la consulta y decidir:
1. ¿Qué tipo de consulta es?
2. ¿Qué municipios involucra (si aplica)?
3. ¿Requiere análisis de datos (código Python)?

Responde ÚNICAMENTE en este formato:
TIPO: [DATA_QUERY | GENERAL | COMPARISON]
MUNICIPIOS: [lista de municipios separados por coma, o "ninguno"]
NECESITA_CODIGO: [SI | NO]

Ejemplos:
- "¿Cuál es el promedio de viento en Riohacha?" 
  → TIPO: DATA_QUERY | MUNICIPIOS: riohacha | NECESITA_CODIGO: SI

- "¿Qué es un modelo LSTM?"
  → TIPO: GENERAL | MUNICIPIOS: ninguno | NECESITA_CODIGO: NO

- "Compara viento entre Riohacha y Maicao"
  → TIPO: COMPARISON | MUNICIPIOS: riohacha, maicao | NECESITA_CODIGO: SI

Consulta del usuario: {query}

Análisis:"""
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def route_query(self, query: str) -> Dict:
        """
        Route the query to appropriate agent(s).
        
        Args:
            query: User's question
            
        Returns:
            Dictionary with routing information
        """
        try:
            response = self.chain.invoke({"query": query})
            
            # Parse response
            lines = response.strip().split('\n')
            routing = {
                "type": "general",
                "municipalities": [],
                "needs_code": False
            }
            
            for line in lines:
                if line.startswith("TIPO:"):
                    tipo = line.split(":", 1)[1].strip().lower()
                    routing["type"] = tipo
                elif line.startswith("MUNICIPIOS:"):
                    munis = line.split(":", 1)[1].strip()
                    if munis.lower() != "ninguno":
                        routing["municipalities"] = [
                            m.strip().lower().replace(" ", "_").replace("á", "a").replace("ó", "o")
                            for m in munis.split(",")
                        ]
                elif line.startswith("NECESITA_CODIGO:"):
                    needs_code = line.split(":", 1)[1].strip().upper()
                    routing["needs_code"] = (needs_code == "SI")
            
            return routing
            
        except Exception as e:
            print(f"{Fore.RED}Error en supervisor: {e}{Style.RESET_ALL}")
            return {
                "type": "general",
                "municipalities": [],
                "needs_code": False
            }

