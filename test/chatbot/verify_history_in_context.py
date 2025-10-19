"""
Script para verificar que el historial se incluye en el contexto del LLM
"""

import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.telegram_bot.mongodb_manager import get_mongodb_manager
from src.telegram_bot.utils import get_user_chain


def verify_history_in_context():
    """Verifica que el historial se cargue y se incluya en el contexto"""
    
    print("="*80)
    print("🔍 VERIFICACIÓN: HISTORIAL EN CONTEXTO DEL LLM")
    print("="*80 + "\n")
    
    mongodb = get_mongodb_manager()
    
    if not mongodb or not mongodb.is_connected:
        print("❌ MongoDB no está conectado")
        print("   Configura MongoDB para usar este script\n")
        return
    
    # Obtener usuarios
    all_users = mongodb.get_all_users()
    
    if not all_users:
        print("⚠️  No hay usuarios en la base de datos")
        print("   Primero interactúa con el bot para crear historial\n")
        return
    
    # Seleccionar primer usuario con historial
    selected_user = None
    for user_id in all_users:
        stats = mongodb.get_user_stats(user_id)
        if stats.get('total_messages', 0) > 0:
            selected_user = user_id
            break
    
    if not selected_user:
        print("⚠️  No hay usuarios con historial\n")
        return
    
    print(f"📊 Usuario seleccionado: {selected_user}\n")
    
    # Obtener el chain (esto cargará el historial automáticamente)
    print("🔄 Creando chain y cargando historial...\n")
    chain = get_user_chain(selected_user)
    
    # Obtener las variables de memoria
    memory_vars = chain.memory.load_memory_variables({})
    history = memory_vars.get('history', '')
    
    if not history:
        print("⚠️  La memoria está vacía (no se cargó historial)\n")
        return
    
    print("✅ HISTORIAL CARGADO EN MEMORIA")
    print("="*80)
    print("\n📝 CONTENIDO DEL HISTORY QUE VERÁ EL LLM:\n")
    print("-"*80)
    print(history)
    print("-"*80)
    
    # Estadísticas
    lines = history.split('\n')
    human_lines = [l for l in lines if l.startswith('Human:')]
    ai_lines = [l for l in lines if l.startswith('AI:')]
    
    print(f"\n📊 ESTADÍSTICAS:")
    print(f"   - Total de líneas: {len(lines)}")
    print(f"   - Mensajes del usuario (Human:): {len(human_lines)}")
    print(f"   - Respuestas del bot (AI:): {len(ai_lines)}")
    print(f"   - Caracteres totales: {len(history)}")
    print(f"   - Tokens estimados: ~{len(history) // 4}")
    
    # Mostrar cómo se vería en el prompt completo
    print("\n" + "="*80)
    print("📄 EJEMPLO DE PROMPT COMPLETO QUE RECIBIRÍA EL LLM")
    print("="*80)
    
    from src.telegram_bot.config import PROMPT
    
    ejemplo_pregunta = "¿Me puedes resumir lo que hemos hablado?"
    
    # Formatear el prompt como lo haría LangChain
    prompt_text = PROMPT.format(
        pregunta=ejemplo_pregunta,
        history=history
    )
    
    # Mostrar primeros 1000 caracteres
    print("\n" + "-"*80)
    if len(prompt_text) > 1000:
        print(prompt_text[:1000])
        print("\n[... {} caracteres más ...]".format(len(prompt_text) - 1000))
    else:
        print(prompt_text)
    print("-"*80)
    
    print("\n✅ VERIFICACIÓN COMPLETA")
    print("\n💡 CONCLUSIÓN:")
    print("   El historial SÍ se incluye en el contexto del LLM.")
    print("   El LLM recibe todo el historial en la sección {history} del prompt.")
    print("   Esto permite respuestas contextualizadas y coherentes.\n")
    
    print("="*80 + "\n")


if __name__ == "__main__":
    verify_history_in_context()

