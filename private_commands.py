import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, MessageHandler, ConversationHandler, filters, CallbackQueryHandler
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


CHOOSE_ACTION, MAIN_MENU, GET_GROUP_ID, GET_USER_ID = range(4)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ['Help', 'Manage'],
        ['Repo', 'Cancel']
    ]
    await update.message.reply_text(
        'Hey! I\'m the Capybara group support bot!\n'
        'Here are some commands you can use!',
        reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    )


async def manage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    manage_keyboard = [
        [InlineKeyboardButton('Add user', callback_data='add_user')],
        [InlineKeyboardButton('Remove user', callback_data='remove_user')]
    ]
    reply_markup = InlineKeyboardMarkup(manage_keyboard)
    await update.message.reply_text('What would you like to do?', reply_markup=reply_markup)
    return CHOOSE_ACTION


async def handle_manage_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    # await query.edit_message_text(f'Selected action: {query.data}')

    if query.data == 'add_user':
        await query.edit_message_text('Please provide the ID of the group you want to manage.')
        context.user_data['action'] = 'add'
        return GET_GROUP_ID

    elif query.data == 'remove_user':
        await query.edit_message_text('Please provide the ID of the group you want to manage.')
        context.user_data['action'] = 'remove'
        return GET_GROUP_ID

    return CHOOSE_ACTION


async def get_group_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        group_id = int(update.message.text)
        user_id = update.effective_user.id

        user_member = await context.bot.get_chat_member(group_id, user_id)
        if user_member.status not in ['administrator', 'creator']:
            await update.message.reply_text('You do not have administrator privileges in this group.')
            return ConversationHandler.END

        context.user_data['group_id'] = group_id
        action = context.user_data['action']
        await update.message.reply_text(f'Privileges confirmed. Please provide the ID of the user you want to {action}.')
        return GET_USER_ID

    except (ValueError, IndexError):
        await update.message.reply_text('Invalid Group ID. Please provide a valid integer ID.')
        return ConversationHandler.END
    except TelegramError as e:
        await update.message.reply_text(f'I cannot access this group. Please make sure I am in the group and have the necessary administrator permissions. Error: {e}')
        return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(f'An error occurred: {e}')
        return ConversationHandler.END


async def get_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        action = context.user_data.get('action')
        group_id = context.user_data.get('group_id')
        user_id = int(update.message.text)

        if action == 'add':
            invite_link = await context.bot.create_chat_invite_link(chat_id=group_id, member_limit=1)
            await update.message.reply_text(f"Here is a single-use invite link for the group:\n{invite_link.invite_link}\nPlease share this link with the user you want to add.")
        elif action == 'remove':
            await context.bot.ban_chat_member(chat_id=group_id, user_id=user_id)
            await update.message.reply_text(f'User {user_id} removed from the group successfully.')

        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text('Invalid User ID. Please provide a valid integer ID.')
        return GET_USER_ID
    except TelegramError as e:
        await update.message.reply_text(f'I could not complete the action. Please make sure I have the necessary permissions. Error: {e}')
        return ConversationHandler.END
    except Exception as e:
        await update.message.reply_text(f'An error occurred: {e}')
        return ConversationHandler.END



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        'Here are some commands you can use:\n'
        '/start — starts the chat with me.\n'
        '/help — returns the list of available commands with their descriptions.\n'
        '/repo — a link to the bot\'s official repository.\n'
        '/manage — manage a group.'
    )
    await update.message.reply_text(help_text)


async def repo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    repo_url = 'https://github.com/yourcatwastaken/TelegramGroupBot'
    message_text = (f'This bot is open source! You can find the code and contribute here:\n ➡️ {repo_url}')
    await update.message.reply_text(message_text)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Command canceled.', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END