import logging
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hey! I\'m the Capybara group support bot!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Here are some commands you can use:\n"
        "/start — starts the chat with me.\n"
        "/help — returns the list of available commands"
    )
    await update.message.reply_text(help_text)