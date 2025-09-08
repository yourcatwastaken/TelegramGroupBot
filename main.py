import os
import logging
from telegram import Update
from telegram.ext import (Application, ApplicationBuilder, CommandHandler, MessageHandler, filters,
    ContextTypes, ConversationHandler, CallbackQueryHandler)
from dotenv import load_dotenv

from admin import delete_service_message, unauthorized
from group_commands import rules, pin
from private_commands import (start, help_command, manage, repo, cancel, sticker,
    get_user_id, get_group_id, handle_manage_choice, CHOOSE_ACTION, GET_GROUP_ID, GET_USER_ID)

# Load the environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# Set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


def get_user_list(env_var_name: str) -> list[int]:
    user_ids_str = os.getenv(env_var_name)
    if not user_ids_str:
        logger.error(f'No {env_var_name} found in environment variables.')
        return []

    user_ids_list = []
    try:
        string_ids = user_ids_str.split(',')
        for uid in string_ids:
            integer_uid = int(uid.strip())
            user_ids_list.append(integer_uid)
        return user_ids_list
    except ValueError:
        logger.error(f"The {env_var_name} variable contains non-integer values.")
        return []

# Load the lists of users
BOT_OWNERS = get_user_list('BOT_OWNERS')
ALLOWED_USERS = get_user_list('USER_IDS')


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling an update:", exc_info=context.error)


def main():
    logger.info('Starting bot...')
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error('No TELEGRAM_BOT_TOKEN found in environment variables.')
        return

    logger.info(f"Bot owners list: {BOT_OWNERS}")
    logger.info(f"Allowed users list: {ALLOWED_USERS}")

    app = ApplicationBuilder().token(token).build()

    # Define filters for the allowed users
    bot_owners_filter = filters.User(user_id=BOT_OWNERS)
    allowed_filter = filters.User(user_id=ALLOWED_USERS)


    manage_conv_handler = ConversationHandler(
        entry_points = [MessageHandler(filters.Regex('^Manage$'), manage)],
        states = {
            CHOOSE_ACTION: [CallbackQueryHandler(handle_manage_choice)],
            GET_GROUP_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_group_id)],
            GET_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_user_id)]
        },
        fallbacks = [MessageHandler(filters.Regex('^Cancel$'), cancel, filters.ChatType.PRIVATE)]
    )
    app.add_handler(manage_conv_handler)


    # Handlers for private chat commands
    app.add_handler(CommandHandler('start', start, filters.ChatType.PRIVATE))
    app.add_handler(MessageHandler(filters.Regex('^Help$'), help_command, filters.ChatType.PRIVATE))
    app.add_handler(MessageHandler(filters.Regex('^Repo$'), repo))
    app.add_handler(MessageHandler(filters.Regex('^Cancel$'), cancel, filters.ChatType.PRIVATE))
    app.add_handler(MessageHandler(filters.Sticker.ALL, sticker, filters.ChatType.PRIVATE))

    # Handlers for groups
    app.add_handler(CommandHandler('rules', rules, filters.ChatType.GROUPS))
    app.add_handler(CommandHandler('pin', pin, filters.ChatType.GROUPS))


    # Handlers for administrator actions. Bot must have necessary permissions
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, delete_service_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.MESSAGE_AUTO_DELETE_TIMER_CHANGED, delete_service_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_PHOTO, delete_service_message))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_TITLE, delete_service_message))

    # Unauthorized user handler
    app.add_handler(MessageHandler(filters.ALL & filters.ChatType.PRIVATE & (~bot_owners_filter) & (~allowed_filter), unauthorized))

    # Error handler
    app.add_error_handler(error_handler)


    logger.info('Polling...')
    # Run the bot until the user presses Ctrl-C
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()