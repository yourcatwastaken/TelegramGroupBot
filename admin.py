import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f'Unauthorized access attempt from user: {update.effective_user.id}')
    await update.message.reply_text('Sorry, you do not have permission to use this bot.')

