import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db():
    return psycopg2.connect(os.getenv("postgresql://postgres:[YOUR-PASSWORD]@db.nkkekmsbekysayxaluqy.supabase.co:5432/postgres"))  # Use your Supabase PostgreSQL URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Talker 👤", callback_data="mode_talker")],
        [InlineKeyboardButton("Listener 👂", callback_data="mode_listener")]
    ]
    await update.message.reply_text(  # <- Closing parenthesis was missing here
        "Choose your role:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )  # <- Now properly closed
    
    # Save user to Supabase
    with get_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (telegram_id)
                VALUES (%s)
                ON CONFLICT (telegram_id) DO NOTHING
            """, (update.effective_user.id,))

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer(f"Selected: {query.data.split('_')[1]} mode")

def main():
    app = Application.builder().token(os.getenv("8219874666:AAHZBrk6t6IzSxOzUI_PlMIZwNcSpXCnR7w")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(set_mode))
    app.run_polling()

if __name__ == "__main__":
    main()
