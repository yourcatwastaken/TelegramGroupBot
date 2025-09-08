import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logger = logging.getLogger(__name__)


async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rules_text = (
        "Group rules:\n"
        "Rule 1...\n"
        "Rule 2..."
    )
    await update.message.reply_text(rules_text)


async def pin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message.reply_to_message:
        try:
            await context.bot.pin_chat_message(
                chat_id=update.effective_chat.id,
                message_id=update.effective_message.reply_to_message.message_id
            )
            logger.info('Message pinned successfully.')
            await update.effective_message.reply_text('Successfully pinned message.')
        except Exception as e:
            await update.effective_message.reply_text(
                'Failed to pin message. Please make sure I have administrator privileges to pin messages in this group.'
            )
            logger.error(f"Failed to pin message: {e}")
    else:
        await update.effective_message.reply_text(
            'Please reply to the message you want to pin with the /pin command.'
        )


async def greet_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await update.message.reply_text(f'Welcome to the group, {member.first_name}')
        sticker_id = 'CAACAgIAAxkBAAESDZNovDL2YMMitnwisa4yleLUOpI3IQACGQAD6dgTKFdhEtpsYKrLNgQ'
        try:
            await update.message.reply_sticker(sticker_id)
        except Exception as e:
            logger.error(f'Failed to send sticker: {e}')