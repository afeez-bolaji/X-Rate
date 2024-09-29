# Main entry point for the bot

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from bot.handlers import start, handle_photo, handle_api_keys, terms_and_policy

def main():
    # Add your bot's token here
    TOKEN = "7837753073:AAGOrCuAv-ql704S7afT47l22BCKRI3jdwA"

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register the command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("terms", terms_and_policy))
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_photo))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_api_keys))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()


