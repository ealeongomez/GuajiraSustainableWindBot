"""
Script para probar la carga de historial desde MongoDB
"""

import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.telegram_bot.mongodb_manager import get_mongodb_manager
from src.telegram_bot.utils import get_user_chain


def test_history_loading():
    """Test que el historial se carga correctamente desde MongoDB"""
    
    print("="*70)
    print("🧪 TEST: CARGA DE HISTORIAL DESDE MONGODB")
    print("="*70 + "\n")
    
    mongodb = get_mongodb_manager()
    
    if not mongodb or not mongodb.is_connected:
        print("❌ MongoDB no está conectado")
        print("   Este test requiere MongoDB configurado")
        return
    
    # Obtener todos los usuarios
    all_users = mongodb.get_all_users()
    
    if not all_users:
        print("⚠️  No hay usuarios en la base de datos")
        print("   Primero interactúa con el bot de Telegram para crear historial")
        return
    
    print(f"✅ Encontrados {len(all_users)} usuarios en MongoDB\n")
    
    # Probar con el primer usuario que tenga historial
    for user_id in all_users:
        stats = mongodb.get_user_stats(user_id)
        total_messages = stats.get('total_messages', 0)
        
        print(f"📊 Usuario {user_id}: {total_messages} mensajes en DB")
        
        if total_messages > 0:
            print(f"\n🔄 Creando chain para usuario {user_id}...")
            print("   (Esto debería cargar las últimas 10 conversaciones)\n")
            
            # Esta llamada debería cargar el historial automáticamente
            chain = get_user_chain(user_id)
            
            # Verificar que la memoria tiene el historial
            memory_vars = chain.memory.load_memory_variables({})
            history = memory_vars.get('history', '')
            
            if history:
                print("✅ ÉXITO: Historial cargado en memoria")
                print(f"\n📝 Historial cargado (primeros 500 chars):")
                print("-" * 70)
                print(history[:500] + "..." if len(history) > 500 else history)
                print("-" * 70)
                
                # Contar líneas
                lines = history.split('\n')
                print(f"\n📊 Líneas en historial: {len(lines)}")
                print(f"📊 Caracteres en historial: {len(history)}")
                
            else:
                print("⚠️  La memoria está vacía (posible error)")
            
            break
    
    print("\n" + "="*70)
    print("✅ Test completado")
    print("="*70 + "\n")
    
    # Instrucciones
    print("💡 NOTA:")
    print("   - El historial se carga automáticamente al primer mensaje de un usuario")
    print("   - Solo se cargan las últimas 10 conversaciones")
    print("   - Usa /clear para limpiar la memoria y recargar desde DB")
    print()


if __name__ == "__main__":
    test_history_loading()

