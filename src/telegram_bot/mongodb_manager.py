"""
MongoDB Manager for Telegram Conversations
"""

import os
from datetime import datetime
from typing import Optional, Dict, List
from pymongo import MongoClient, DESCENDING
from pymongo.errors import ConnectionFailure


class MongoDBManager:
    """
    Manages MongoDB operations for storing Telegram conversations.
    """
    
    def __init__(self):
        """Initialize MongoDB connection"""
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self.db_name = os.getenv("MONGODB_DATABASE", "windbot_telegram")
        self.collection_name = "conversations"
        
        self.client: Optional[MongoClient] = None
        self.db = None
        self.collection = None
        self.is_connected = False
        
        self._connect()
    
    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            
            self.db = self.client[self.db_name]
            self.collection = self.db[self.collection_name]
            self.is_connected = True
            
            # Create indexes
            self.collection.create_index("user_id")
            self.collection.create_index("timestamp")
            
            print(f"✅ MongoDB conectado: {self.db_name}")
            
        except ConnectionFailure as e:
            print(f"⚠️  MongoDB no disponible: {e}")
            print("   Las conversaciones no se guardarán en base de datos")
            self.is_connected = False
        except Exception as e:
            print(f"⚠️  Error conectando a MongoDB: {e}")
            self.is_connected = False
    
    def save_conversation(
        self,
        user_id: int,
        user_name: str,
        user_message: str,
        bot_response: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Save a conversation to MongoDB.
        
        Args:
            user_id: Telegram user ID
            user_name: User's first name
            user_message: User's message
            bot_response: Bot's response
            metadata: Optional additional metadata
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        if not self.is_connected:
            return False
        
        try:
            document = {
                "user_id": user_id,
                "user_name": user_name,
                "user_message": user_message,
                "bot_response": bot_response,
                "timestamp": datetime.utcnow(),
                "platform": "telegram",
                "metadata": metadata or {}
            }
            
            self.collection.insert_one(document)
            return True
            
        except Exception as e:
            print(f"❌ Error guardando conversación: {e}")
            return False
    
    def get_user_history(
        self,
        user_id: int,
        limit: int = 10
    ) -> List[Dict]:
        """
        Get conversation history for a specific user.
        
        Args:
            user_id: Telegram user ID
            limit: Number of conversations to retrieve
            
        Returns:
            List of conversation documents
        """
        if not self.is_connected:
            return []
        
        try:
            conversations = self.collection.find(
                {"user_id": user_id}
            ).sort("timestamp", DESCENDING).limit(limit)
            
            return list(conversations)
            
        except Exception as e:
            print(f"❌ Error obteniendo historial: {e}")
            return []
    
    def get_user_stats(self, user_id: int) -> Dict:
        """
        Get statistics for a specific user.
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            Dictionary with user statistics
        """
        if not self.is_connected:
            return {}
        
        try:
            total_messages = self.collection.count_documents({"user_id": user_id})
            
            first_interaction = self.collection.find_one(
                {"user_id": user_id},
                sort=[("timestamp", 1)]
            )
            
            last_interaction = self.collection.find_one(
                {"user_id": user_id},
                sort=[("timestamp", -1)]
            )
            
            return {
                "total_messages": total_messages,
                "first_interaction": first_interaction.get("timestamp") if first_interaction else None,
                "last_interaction": last_interaction.get("timestamp") if last_interaction else None
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo estadísticas: {e}")
            return {}
    
    def get_all_users(self) -> List[int]:
        """
        Get list of all unique user IDs.
        
        Returns:
            List of user IDs
        """
        if not self.is_connected:
            return []
        
        try:
            user_ids = self.collection.distinct("user_id")
            return user_ids
            
        except Exception as e:
            print(f"❌ Error obteniendo usuarios: {e}")
            return []
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")


# Global instance
mongodb_manager: Optional[MongoDBManager] = None


def get_mongodb_manager() -> Optional[MongoDBManager]:
    """
    Get or create the global MongoDB manager instance.
    
    Returns:
        MongoDBManager instance or None if MongoDB is not configured
    """
    global mongodb_manager
    
    if mongodb_manager is None:
        mongodb_manager = MongoDBManager()
    
    return mongodb_manager if mongodb_manager.is_connected else None

