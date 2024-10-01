from telegram.ext import Application, CommandHandler, MessageHandler, filters
from handlers import start, handle_photo, handle_api_keys, terms_and_policy
import os
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    TOKEN = os.getenv("TOKEN")  # Make sure TOKEN is loaded correctly from .env

    # Initialize the application (replaces Updater in version 20+)
    application = Application.builder().token(TOKEN).build()

    # Register the command and message handlers (all functions are now async)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("terms", terms_and_policy))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_api_keys))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
