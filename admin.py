import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f'Unauthorized access attempt from user: {update.effective_user.id}')
    await update.message.reply_text('Sorry, you do not have permission to use this bot.')

async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Deletes service messages. The bot must have administrator privileges
    try:
        await update.message.delete()
        logging.info('Service message deleted successfully.')
    except Exception as e:
        logging.error(f'Failed to delete service message: {e}')