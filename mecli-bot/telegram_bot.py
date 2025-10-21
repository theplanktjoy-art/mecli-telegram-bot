import os
import sys
import logging
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('8211808352:AAG3ZvQyOhNb12LsZVOxNWapZ8z4TGbLgxc')
API_KEY = os.environ.get('85236672-82e0-40f3-8477-4346650e9a18', '')

# User state storage
user_states = {}

async def start(update Update, context ContextTypes.DEFAULT_TYPE)
    Send a message when the command start is issued.
    welcome_message = 
🤖 Selamat datang di ME-CLI Bot!

Bot ini adalah wrapper untuk me-cli tool.

Perintah yang tersedia
start - Menampilkan pesan ini
setkey - Set API key Anda
run - Menjalankan me-cli
help - Bantuan penggunaan
status - Cek status bot

_Pertama kali gunakan setkey untuk mengatur API key Anda._
    
    await update.message.reply_text(welcome_message, parse_mode='Markdown')

async def help_command(update Update, context ContextTypes.DEFAULT_TYPE)
    Send a message when the command help is issued.
    help_text = 
📖 Panduan Penggunaan

1️⃣ Dapatkan API key dari @fykxt_bot dengan mengirim viewkey
2️⃣ Set API key Anda setkey
3️⃣ Jalankan bot run
4️⃣ Bot akan memproses request Anda

Catatan
- API key bersifat pribadi, jangan dibagikan
- Setiap user memiliki API key sendiri
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def setkey(update Update, context ContextTypes.DEFAULT_TYPE)
    Set API key for user.
    user_id = update.effective_user.id
    user_states[user_id] = 'waiting_for_key'
    
    await update.message.reply_text(
        🔑 Silakan kirim API key Anda.n
        Dapatkan API key dari @fykxt_bot dengan mengirim viewkeynn
        Kirim API key Anda sekarang
    )

async def status(update Update, context ContextTypes.DEFAULT_TYPE)
    Check bot status.
    user_id = update.effective_user.id
    has_key = user_id in user_states and 'api_key' in user_states[user_id]
    
    status_text = f
📊 Status Bot

User ID `{user_id}`
API Key {✅ Sudah diset if has_key else ❌ Belum diset}
Bot Status 🟢 Online

{Anda sudah bisa menggunakan run if has_key else Gunakan setkey untuk mengatur API key}
    
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def run_mecli(update Update, context ContextTypes.DEFAULT_TYPE)
    Run the me-cli script.
    user_id = update.effective_user.id
    
    # Check if user has set API key
    if user_id not in user_states or 'api_key' not in user_states[user_id]
        await update.message.reply_text(
            ❌ Anda belum mengatur API key!n
            Gunakan setkey terlebih dahulu.
        )
        return
    
    api_key = user_states[user_id]['api_key']
    
    await update.message.reply_text(⏳ Memproses request Anda...)
    
    try
        # Run the me-cli script
        process = subprocess.Popen(
            ['python', 'main.py'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd='appme-cli'  # Adjust path if needed
        )
        
        # Send API key to stdin
        stdout, stderr = process.communicate(input=api_key + 'n', timeout=30)
        
        if process.returncode == 0
            result = stdout if stdout else ✅ Proses selesai!
            # Split long messages
            if len(result)  4000
                for i in range(0, len(result), 4000)
                    await update.message.reply_text(f```n{result[ii+4000]}n```, parse_mode='Markdown')
            else
                await update.message.reply_text(f```n{result}n```, parse_mode='Markdown')
        else
            error_msg = stderr if stderr else Unknown error
            await update.message.reply_text(f❌ Errorn```n{error_msg}n```, parse_mode='Markdown')
            
    except subprocess.TimeoutExpired
        process.kill()
        await update.message.reply_text(❌ Request timeout! Silakan coba lagi.)
    except Exception as e
        logger.error(fError running me-cli {e})
        await update.message.reply_text(f❌ Terjadi kesalahan {str(e)})

async def handle_message(update Update, context ContextTypes.DEFAULT_TYPE)
    Handle text messages (for API key input).
    user_id = update.effective_user.id
    text = update.message.text
    
    # Check if user is in key setting state
    if user_id in user_states and user_states[user_id] == 'waiting_for_key'
        # Store the API key
        if user_id not in user_states
            user_states[user_id] = {}
        user_states[user_id]['api_key'] = text.strip()
        user_states[user_id]['state'] = 'key_set'
        
        await update.message.reply_text(
            ✅ API key berhasil disimpan!nn
            Sekarang Anda bisa menggunakan run untuk menjalankan me-cli.
        )
    else
        await update.message.reply_text(
            Gunakan perintah help untuk melihat daftar perintah yang tersedia.
        )

async def error_handler(update Update, context ContextTypes.DEFAULT_TYPE)
    Log errors caused by updates.
    logger.error(fUpdate {update} caused error {context.error})

def main()
    Start the bot.
    if not BOT_TOKEN
        logger.error(BOT_TOKEN environment variable not set!)
        sys.exit(1)
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register handlers
    application.add_handler(CommandHandler(start, start))
    application.add_handler(CommandHandler(help, help_command))
    application.add_handler(CommandHandler(setkey, setkey))
    application.add_handler(CommandHandler(run, run_mecli))
    application.add_handler(CommandHandler(status, status))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register error handler
    application.add_error_handler(error_handler)
    
    # Start the bot
    logger.info(Bot started!)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__'
    main()