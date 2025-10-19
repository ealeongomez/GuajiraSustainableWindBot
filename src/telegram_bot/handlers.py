"""
Telegram Bot Handlers
"""

from telegram import Update
from telegram.ext import ContextTypes
from langsmith import traceable
from .utils import get_user_chain, clear_user_memory
from .mongodb_manager import get_mongodb_manager


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command and identify user"""
    user = update.effective_user
    telegram_id = user.id
    first_name = user.first_name or "Usuario"

    print(f"{telegram_id}")

    welcome_message = (
        f"🌬️ ¡Hola {first_name}!\n\n"
        f"Soy *WindBot*, tu asistente de predicción de viento en La Guajira.\n\n"
        f"🆔 Tu ID único: `{telegram_id}`\n\n"
        f"Puedo ayudarte con:\n"
        f"• Predicciones de viento\n"
        f"• Información de los 13 municipios\n"
        f"• Energía sostenible\n"
        f"• Modelos LSTM y RFF\n\n"
        f"Comandos disponibles:\n"
        f"/start - Mostrar este mensaje\n"
        f"/help - Ayuda\n"
        f"/clear - Limpiar historial\n\n"
        f"¡Hazme cualquier pregunta sobre el clima o energía eólica!"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    user_id = update.effective_user.id
    print(f"{user_id}")
    
    help_message = (
        "📖 *Ayuda - WindBot*\n\n"
        "Comandos disponibles:\n"
        "/start - Mensaje de bienvenida\n"
        "/help - Mostrar esta ayuda\n"
        "/clear - Limpiar historial de conversación\n\n"
        "Ejemplos de preguntas:\n"
        "• ¿Qué velocidad del viento hay en Riohacha?\n"
        "• ¿Qué modelos usas para predicción?\n"
        "• ¿Cuál es el potencial eólico de Maicao?\n"
        "• ¿Qué municipios monitoreas?"
    )
    await update.message.reply_text(help_message, parse_mode="Markdown")


async def clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /clear command to reset user memory"""
    user_id = update.effective_user.id
    print(f"{user_id}")
    
    # Clear in-memory cache (next message will reload from MongoDB)
    clear_user_memory(user_id)
    
    await update.message.reply_text(
        "✅ Historial en memoria limpiado.\n"
        "💾 Las conversaciones permanecen guardadas en la base de datos.\n"
        "Al enviar tu próximo mensaje, se cargarán las últimas 10 conversaciones."
    )


@traceable(name="telegram_message_handler", tags=["telegram", "user_message"])
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages with LangSmith tracing and MongoDB storage"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Usuario"
    user_message = update.message.text.strip()

    print(f"{user_id}")

    # Mostrar typing
    await update.message.chat.send_action(action="typing")

    try:
        # Get or create user chain
        chain = get_user_chain(user_id)

        # Generate LLM response with tracing metadata
        response = chain.invoke(
            {"pregunta": user_message},
            config={
                "tags": ["telegram", f"user_{user_id}"],
                "metadata": {
                    "user_id": user_id,
                    "platform": "telegram"
                }
            }
        )
        bot_reply = response["text"]

        # Send response
        await update.message.reply_text(bot_reply)
        
        # Save conversation to MongoDB with unique ID
        mongodb = get_mongodb_manager()
        if mongodb:
            conversation_id = mongodb.save_conversation(
                user_id=user_id,
                user_name=user_name,
                user_message=user_message,
                bot_response=bot_reply,
                metadata={
                    "username": update.effective_user.username,
                    "chat_id": update.message.chat_id
                }
            )
            if conversation_id:
                print(f"💾 {conversation_id}")

    except Exception as e:
        print(f"{user_id}")
        await update.message.reply_text(
            "⚠️ Ocurrió un error procesando tu mensaje. Intenta de nuevo o usa /help."
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """General error handler"""
    print(f"⚠️ Error en bot: {context.error}")
    if update and update.message:
        await update.message.reply_text("❌ Ha ocurrido un error. Intenta nuevamente más tarde.")

