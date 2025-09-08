import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logger = logging.getLogger(__name__)


# Deletes service messages. The bot must have administrator privileges
async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
        logger.info('Service message deleted successfully.')
    except Exception as e:
        logger.error(f'Failed to delete service message: {e}')


async def unauthorized(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f'Unauthorized access attempt from user: {update.effective_user.id}')
    await update.message.reply_text('Sorry, you do not have permission to use this bot.')

