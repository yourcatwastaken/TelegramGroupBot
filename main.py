import os
import logging
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

from admin import unauthorized
from group_commands import delete_service_message, rules
from private_commands import start, help_command
# Load the environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def get_allowed_users():
    user_ids_str = os.getenv('USER_IDS')
    if not user_ids_str:
        logging.error('No USER_IDS found in environment variables.')
        return []
    allowed_users_list = []
    try:
        user_ids_list = user_ids_str.split(',')
        for uid in user_ids_list:
            integer_uid = int(uid.strip())
            allowed_users_list.append(integer_uid)
        return allowed_users_list
    except ValueError:
        logging.error("The USER_IDS variable contains non-integer values.")
        return []

ALLOWED_USERS = get_allowed_users()

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Exception while handling an update:", exc_info=context.error)


def main():
    print('Starting bot...')
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logging.error('No TELEGRAM_BOT_TOKEN found in environment variables.')
        return

    print(f"Allowed users list: {ALLOWED_USERS}")

    app = ApplicationBuilder().token(token).build()

    # Define a filter for the allowed users
    allowed_filter = filters.User(user_id=ALLOWED_USERS)

    # Handlers for private chats (whitelisted users)
    app.add_handler(CommandHandler('start', start, filters=allowed_filter & filters.ChatType.PRIVATE))
    app.add_handler(CommandHandler('help', help_command, filters=allowed_filter & filters.ChatType.PRIVATE))

    # Group commands
    app.add_handler(CommandHandler('rules', rules, filters.ChatType.GROUPS))


   # TODO:add /pin command


    # Unauthorized user handler
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE & (~allowed_filter), unauthorized))

    # Handlers for administrator actions. Bot must have necessary permissions
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, delete_service_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, delete_service_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.MESSAGE_AUTO_DELETE_TIMER_CHANGED, delete_service_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_PHOTO, delete_service_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_TITLE, delete_service_message))

    # Error handler
    app.add_error_handler(error_handler)


    print('Polling...')
    # Run the bot until the user presses Ctrl-C
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()