"""
Script de ejemplo para consultar conversaciones guardadas en MongoDB
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.telegram_bot.mongodb_manager import get_mongodb_manager


def main():
    print("="*70)
    print("📊 CONSULTA DE CONVERSACIONES EN MONGODB")
    print("="*70 + "\n")
    
    mongodb = get_mongodb_manager()
    
    if not mongodb or not mongodb.is_connected:
        print("❌ MongoDB no está conectado")
        print("   Verifica tu configuración en .env")
        return
    
    print("✅ Conectado a MongoDB\n")
    
    # 1. Estadísticas generales
    print("1️⃣  ESTADÍSTICAS GENERALES")
    print("-" * 70)
    
    all_users = mongodb.get_all_users()
    print(f"   Total de usuarios: {len(all_users)}")
    
    for user_id in all_users:
        stats = mongodb.get_user_stats(user_id)
        print(f"   Usuario {user_id}: {stats['total_messages']} mensajes")
    
    print()
    
    # 2. Últimas 10 conversaciones
    print("2️⃣  ÚLTIMAS 10 CONVERSACIONES")
    print("-" * 70)
    
    recent = mongodb.search_conversations(limit=10)
    
    for conv in recent:
        timestamp = conv['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
        conv_id = conv['conversation_id'][:8] + "..."
        user = conv['user_name']
        message = conv['user_message'][:50] + "..." if len(conv['user_message']) > 50 else conv['user_message']
        
        print(f"   [{timestamp}] {conv_id} - {user}")
        print(f"   💬 {message}\n")
    
    # 3. Conversaciones de las últimas 24 horas
    print("3️⃣  CONVERSACIONES DE LAS ÚLTIMAS 24 HORAS")
    print("-" * 70)
    
    start_date = datetime.utcnow() - timedelta(hours=24)
    recent_24h = mongodb.search_conversations(start_date=start_date)
    
    print(f"   Total: {len(recent_24h)} conversaciones\n")
    
    for conv in recent_24h[:5]:  # Mostrar solo 5
        timestamp = conv['timestamp'].strftime('%H:%M:%S')
        user = conv['user_name']
        print(f"   [{timestamp}] {user}: {conv['user_message'][:60]}...")
    
    print()
    
    # 4. Buscar por usuario específico
    if all_users:
        print("4️⃣  HISTORIAL DE UN USUARIO ESPECÍFICO")
        print("-" * 70)
        
        user_id = all_users[0]
        user_history = mongodb.get_user_history(user_id, limit=5)
        
        print(f"   Usuario: {user_id}")
        print(f"   Últimas {len(user_history)} interacciones:\n")
        
        for conv in user_history:
            timestamp = conv['timestamp'].strftime('%Y-%m-%d %H:%M')
            print(f"   [{timestamp}]")
            print(f"   👤 Usuario: {conv['user_message']}")
            print(f"   🤖 Bot: {conv['bot_response'][:80]}...")
            print(f"   🔗 ID: {conv['conversation_id']}\n")
    
    # 5. Buscar conversación específica por ID
    print("5️⃣  BUSCAR POR CONVERSATION_ID")
    print("-" * 70)
    print("   Uso:")
    print("   conversation = mongodb.get_conversation_by_id('a7b3c4d5-...')")
    print()
    
    mongodb.close()
    print("="*70)
    print("✅ Consulta completada")
    print("="*70)


if __name__ == "__main__":
    main()

