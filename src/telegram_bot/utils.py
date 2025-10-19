"""
Utility functions for Telegram Bot
"""

from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from .config import LLM, PROMPT, USER_MEMORIES
from .mongodb_manager import get_mongodb_manager


def load_user_history_from_db(user_id: int, memory: ConversationBufferMemory, max_messages: int = 10):
    """
    Load user's conversation history from MongoDB into memory.
    
    Args:
        user_id (int): Telegram user ID
        memory (ConversationBufferMemory): Memory object to populate
        max_messages (int): Maximum number of historical messages to load (default: 10)
    """
    mongodb = get_mongodb_manager()
    
    if not mongodb or not mongodb.is_connected:
        return
    
    try:
        # Get last N conversations from MongoDB
        history = mongodb.get_user_history(user_id, limit=max_messages)
        
        if not history:
            return
        
        # Reverse to get chronological order (oldest first)
        history.reverse()
        
        # Load each conversation into memory
        for conv in history:
            user_message = conv.get("user_message", "")
            bot_response = conv.get("bot_response", "")
            
            if user_message and bot_response:
                # Add to memory buffer
                memory.save_context(
                    {"pregunta": user_message},
                    {"text": bot_response}
                )
        
        print(f"📚 Cargados {len(history)} mensajes históricos para usuario {user_id}")
        
    except Exception as e:
        print(f"⚠️  Error cargando historial para usuario {user_id}: {e}")


def get_user_chain(user_id: int) -> LLMChain:
    """
    Retrieve or create a conversational chain for a specific user.
    Each Telegram user has its own memory identified by telegram_id.
    
    Loads the last 10 conversations from MongoDB to maintain context
    across bot restarts.
    
    Args:
        user_id (int): Telegram user ID
        
    Returns:
        LLMChain: Conversation chain with memory for the user
    """
    if user_id not in USER_MEMORIES:
        # Create new memory for this user
        memory = ConversationBufferMemory(input_key="pregunta", memory_key="history")
        
        # Load historical conversations from MongoDB (max 10)
        load_user_history_from_db(user_id, memory, max_messages=10)
        
        # Create chain with memory
        USER_MEMORIES[user_id] = LLMChain(
            prompt=PROMPT,
            llm=LLM,
            memory=memory
        )
    
    return USER_MEMORIES[user_id]


def clear_user_memory(user_id: int):
    """
    Clear the in-memory conversation history for a specific user.
    This does not delete conversations from MongoDB.
    
    Args:
        user_id (int): Telegram user ID
    """
    if user_id in USER_MEMORIES:
        del USER_MEMORIES[user_id]
        print(f"🧹 Memoria limpiada para usuario {user_id}")

