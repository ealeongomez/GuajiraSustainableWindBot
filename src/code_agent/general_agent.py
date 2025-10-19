"""
General Agent - Handles conceptual questions without code
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


class GeneralAgent:
    """General agent for conceptual questions (no code execution)."""
    
    def __init__(self, llm):
        """
        Initialize General Agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
        
        self.prompt = ChatPromptTemplate.from_template(
            """Eres WindBot, un asistente experto en predicción de viento y energía sostenible en La Guajira, Colombia.

Monitoras 13 municipios: Albania, Barrancas, Distracción, El Molino, Fonseca, Hatonuevo, 
La Jagua del Pilar, Maicao, Manaure, Mingueo, Riohacha, San Juan del Cesar y Uribia.

Responde preguntas generales sobre:
- Energía eólica y sostenibilidad
- Modelos de predicción LSTM y Deep Learning
- Conceptos técnicos sobre viento y meteorología
- Información general sobre La Guajira

Responde ÚNICAMENTE en español de forma clara, técnica pero accesible.

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

