import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db():
    # Fixed: Use os.getenv() properly with just the environment variable name
    return psycopg2.connect(os.getenv("postgresql://postgres:[YOUR-PASSWORD]@db.nkkekmsbekysayxaluqy.supabase.co:5432/postgres"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Talker 👤", callback_data="mode_talker")],
        [InlineKeyboardButton("Listener 👂", callback_data="mode_listener")]
    ]
    await update.message.reply_text(
        "Choose your role:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    
    # Save user to database
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO users (telegram_id)
                    VALUES (%s)
                    ON CONFLICT (telegram_id) DO NOTHING
                """, (update.effective_user.id,))
                conn.commit()
    except Exception as e:
        print(f"Database error: {e}")

async def set_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    mode = query.data.split('_')[1].capitalize()
    await query.answer(f"Selected: {mode} mode")
    
    # Update user's mode in database
    try:
        with get_db() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE users 
                    SET mode = %s 
                    WHERE telegram_id = %s
                """, (query.data.split('_')[1], update.effective_user.id))
                conn.commit()
    except Exception as e:
        print(f"Database error: {e}")

def main():
    # Fixed: Use os.getenv() properly with just the environment variable name
    app = Application.builder().token(os.getenv("8219874666:AAG2fA_OBnFpSCrbyz8J8405-tuNnRG1ttw")).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(set_mode))
    
    print("Bot is starting...")
    app.run_polling()

# Fixed: Proper __name__ check
if __name__ == "__main__":
    main()
