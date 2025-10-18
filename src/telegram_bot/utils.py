"""
Utility functions for Telegram Bot
"""

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from .config import LLM, PROMPT, USER_MEMORIES


def get_user_chain(user_id: int) -> LLMChain:
    """
    Retrieve or create a conversational chain for a specific user.
    Each Telegram user has its own memory identified by telegram_id.
    
    Args:
        user_id (int): Telegram user ID
        
    Returns:
        LLMChain: Conversation chain with memory for the user
    """
    if user_id not in USER_MEMORIES:
        memory = ConversationBufferMemory(input_key="pregunta", memory_key="history")
        USER_MEMORIES[user_id] = LLMChain(
            prompt=PROMPT,
            llm=LLM,
            memory=memory
        )
    return USER_MEMORIES[user_id]

