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
            """Eres WindBot, un asistente especializado EXCLUSIVAMENTE en predicción de viento y energía sostenible en La Guajira, Colombia.

IMPORTANTE - RESTRICCIONES ESTRICTAS:
1. SOLO respondes sobre La Guajira, Colombia
2. SOLO sobre estos 13 municipios: Albania, Barrancas, Distracción, El Molino, Fonseca, Hatonuevo, La Jagua del Pilar, Maicao, Manaure, Mingueo, Riohacha, San Juan del Cesar y Uribia
3. SOLO sobre estos temas: energía eólica, predicción de viento, modelos LSTM, sostenibilidad energética
4. NO respondas sobre otros lugares, temas políticos, entretenimiento, o cualquier tema fuera de tu especialidad

Si la pregunta está fuera de tu dominio, responde:
"Lo siento, solo puedo ayudarte con información sobre predicción de viento y energía eólica en La Guajira, Colombia."

Temas que PUEDES responder:
- Energía eólica y sostenibilidad
- Modelos de predicción LSTM y Deep Learning aplicados al viento
- Conceptos técnicos sobre viento y meteorología
- Información general sobre La Guajira relacionada con energía eólica

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

