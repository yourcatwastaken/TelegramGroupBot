import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def delete_service_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Deletes service messages. The bot must have administrator privileges
    try:
        await update.message.delete()
        logging.info('Service message deleted successfully.')
    except Exception as e:
        logging.error(f'Failed to delete service message: {e}')


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = (
        "Group rules:\n"
        "Rule 1...\n"
        "Rule 2..."
    )
    await update.message.reply_text(rules_text)