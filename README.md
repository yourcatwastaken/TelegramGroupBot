# Group Support Bot
This is a Telegram bot designed to help with group management. It is built using the `python-telegram-bot` library and features a whitelisting system for access control and admin-level functionality to automatically delete specific service messages.

## Features
* **Whitelisting:** Only pre-approved users are allowed to use the bot's commands.
* **Admin Control:** Automatically deletes various service messages (e.g., a user leaving or joining) in a group to keep the chat clean.
* **Modularity:** The bot's functionality is split into separate files for clean and scalable code.

## Installation and Setup

### 1. Prerequisites
* Python 3.9+
* ```pip``` (Python package installer)

### 2. Environment Variables
Create a file named .env in the root directory of the project and add your Telegram bot token and the user IDs you want to whitelist.
``` 
TELEGRAM_BOT_TOKEN="YOUR_TOKEN"
USER_IDS="123456789,987654321" 
```

### 3. Install Dependencies
Install the required Python libraries using the following command:
```
pip install python-telegram-bot python-dotenv
```

### 4. Run the Bot
To start the bot, run the main.py file from your terminal:
```
python main.py
```

## Admin Functionality
For the bot's admin features to work, you must add the bot to a group and grant it administrator privileges with the "Delete Messages" permission. Without this permission, the bot won't be able to delete service messages and will log an error.