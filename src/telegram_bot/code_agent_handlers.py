"""
Telegram Bot Handlers for Code Multi-Agent System
==================================================

Handlers for the text-to-python multi-agent system with Telegram frontend.
Uses CodeMultiAgentSystem for zero-hallucination data analysis.

Author: Eder Arley León Gómez
Created on: 2025-10-19
"""

from telegram import Update
from telegram.ext import ContextTypes
from langsmith import traceable
from .mongodb_manager import get_mongodb_manager


# Global instance of the multi-agent system (initialized on first use)
_code_agent_system = None


def get_code_agent_system():
    """Get or create the CodeMultiAgentSystem instance"""
    global _code_agent_system
    if _code_agent_system is None:
        try:
            from src.code_agent import CodeMultiAgentSystem
            _code_agent_system = CodeMultiAgentSystem(verbose=False)
            print("✅ CodeMultiAgentSystem inicializado")
        except Exception as e:
            print(f"❌ Error inicializando CodeMultiAgentSystem: {e}")
            raise
    return _code_agent_system


async def start_command_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command for code agent bot"""
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name or "Usuario"

    print(f"🆔 Usuario conectado: {telegram_id}")

    welcome_message = (
        f"🌬️ ¡Hola {first_name}!\n\n"
        f"Soy *WindBot Code Agent*, tu asistente avanzado de análisis de viento en La Guajira.\n\n"
        f"🆔 Tu ID único: `{telegram_id}`\n\n"
        f"🐍 *Sistema Multi-Agente con Python*\n"
        f"• 1 Supervisor + 13 Agentes municipales + 1 Agente general\n"
        f"• Generación y ejecución de código Python\n"
        f"• Zero alucinaciones en datos numéricos\n"
        f"• Análisis preciso con estadísticas y gráficos\n\n"
        f"Puedo ayudarte con:\n"
        f"• Análisis estadístico de viento por municipio\n"
        f"• Generación de gráficos y visualizaciones\n"
        f"• Comparativas entre municipios\n"
        f"• Predicciones y tendencias\n"
        f"• Información conceptual sobre energía eólica\n\n"
        f"Comandos disponibles:\n"
        f"/start - Mostrar este mensaje\n"
        f"/help - Ayuda detallada\n"
        f"/clear - Limpiar historial\n\n"
        f"¡Hazme cualquier pregunta sobre análisis de viento!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command for code agent bot"""
    user_id = update.effective_user.id
    print(f"📖 Ayuda solicitada por usuario: {user_id}")
    
    help_message = (
        "📖 *Ayuda - WindBot Code Agent*\n\n"
        "🤖 *Sistema Multi-Agente*\n"
        "Este bot usa un sistema de 15 agentes especializados:\n"
        "• 1 Supervisor que enruta las consultas\n"
        "• 13 Agentes para cada municipio (Albania, Barrancas, etc.)\n"
        "• 1 Agente general para preguntas conceptuales\n\n"
        "🐍 *Capacidades de Código*\n"
        "• Genera código Python para análisis\n"
        "• Ejecuta código de forma segura\n"
        "• Crea gráficos y estadísticas\n"
        "• Zero alucinaciones en datos numéricos\n\n"
        "📊 *Ejemplos de preguntas:*\n"
        "• ¿Cuál es la velocidad promedio del viento en Riohacha?\n"
        "• Muéstrame un gráfico de viento en Maicao\n"
        "• Compara las velocidades entre Albania y Fonseca\n"
        "• ¿Qué es la energía eólica?\n"
        "• ¿Cuál municipio tiene mayor potencial eólico?\n\n"
        "⚙️ *Comandos:*\n"
        "/start - Mensaje de bienvenida\n"
        "/help - Mostrar esta ayuda\n"
        "/clear - Limpiar historial de conversación\n\n"
        "💡 *Nota:* Los gráficos se guardan en `test/chatbot/output/`"
    )
    await update.message.reply_text(help_message, parse_mode="Markdown")


async def clear_command_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command for code agent bot"""
    user_id = update.effective_user.id
    print(f"🧹 Historial limpiado para usuario: {user_id}")
    
    await update.message.reply_text(
        "✅ Historial limpiado.\n"
        "💾 Las conversaciones permanecen guardadas en la base de datos.\n"
        "📝 El próximo mensaje iniciará una nueva conversación."
    )


@traceable(name="telegram_code_agent_handler", tags=["telegram", "code_agent", "multiagent"])
async def handle_message_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages with CodeMultiAgentSystem"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Usuario"
    user_message = update.message.text.strip()

    print(f"\n{'='*80}")
    print(f"👤 Usuario {user_id}: {user_message}")
    print(f"{'='*80}\n")

    # Mostrar typing
    await update.message.chat.send_action(action="typing")

    try:
        # Get or create the code agent system
        system = get_code_agent_system()

        # Process the query with the multi-agent system
        response = system.process_query(user_message, verbose=False)

        # Send response
        await update.message.reply_text(response)
        
        print(f"\n{'='*80}")
        print(f"🤖 Bot respondió a usuario {user_id}")
        print(f"{'='*80}\n")
        
        # Save conversation to MongoDB
        mongodb = get_mongodb_manager()
        if mongodb:
            conversation_id = mongodb.save_conversation(
                user_id=user_id,
                user_name=user_name,
                user_message=user_message,
                bot_response=response,
                metadata={
                    "username": update.effective_user.username,
                    "chat_id": update.message.chat_id,
                    "bot_type": "code_agent"
                }
            )
            if conversation_id:
                print(f"💾 Conversación guardada: {conversation_id}\n")

    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error procesando mensaje de usuario {user_id}: {error_msg}\n")
        await update.message.reply_text(
            "⚠️ Ocurrió un error procesando tu mensaje.\n"
            "Intenta reformular tu pregunta o usa /help para ver ejemplos."
        )


async def error_handler_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """General error handler for code agent bot"""
    print(f"⚠️ Error en bot: {context.error}")
    if update and update.message:
        await update.message.reply_text(
            "❌ Ha ocurrido un error interno.\n"
            "Por favor intenta nuevamente más tarde."
        )

