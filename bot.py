from telegram.ext import Updater, CommandHandler
import os
from dotenv import load_dotenv, find_dotenv
from command_handlers import (
    code_command_handler,
    help_command_handler,
)

load_dotenv(find_dotenv())

def get_text_from_callback(update):
    return update.callback_query.data

def main():
    updater = Updater(os.environ.get("TELEGRAM_TOKEN", ""), use_context=True)
    dp = updater.dispatcher
    # command handlers
    dp.add_handler(CommandHandler("help", help_command_handler))
    dp.add_handler(CommandHandler("start", help_command_handler))
    dp.add_handler(CommandHandler("code", code_command_handler))

    ENV = os.environ.get("ENV", "")
    if ENV == "production":
        # Start the webhook
        TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
        NAME = os.environ.get("NAME", "")
        PORT = int(os.environ.get("PORT", 5000))
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN,
            webhook_url=f"https://{NAME}.herokuapp.com/{TOKEN}",
        )
        updater.idle()
    elif ENV == "development":
        print("Bot is running locally...Press Ctrl-C to quit.")
        # start polling
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    load_dotenv(find_dotenv())
    main()
