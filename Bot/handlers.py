# Handlers for different bot commands and messages

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from bot.keyboards import bybit_registration_keyboard

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username
    first_name = user.first_name

    # Greeting the user
    welcome_message = f"Hello, {first_name} (@{username})! Welcome to XRate P2P Trading Bot. You need to sign up on Bybit to use our services."
    update.message.reply_text(welcome_message)

    # Providing registration link and description
    description = ("Please sign up on Bybit using the following link:\n\n"
                   "1. Visit the Bybit registration page.\n"
                   "2. Complete the registration form.\n"
                   "3. Verify your identity as required.\n"
                   "4. Once you're signed up, go to your profile, and generate your API key and secret key.\n"
                   "5. Send your API and secret keys to this bot for trading.")
    update.message.reply_text(description, reply_markup=bybit_registration_keyboard())

def terms_and_policy(update: Update, context: CallbackContext):
    # Terms and policy message
    terms = ("Terms of Service:\n\n"
             "1. All users must comply with Bybit's terms and conditions.\n"
             "2. P2P transactions are subject to market risk.\n"
             "3. We do not hold responsibility for losses incurred through trading.\n\n"
             "By using our services, you agree to these terms.")
    update.message.reply_text(terms)

def handle_photo(update: Update, context: CallbackContext):
    # Handling user photo uploads (face and passport)
    update.message.reply_text("Thank you for uploading your document. You can now proceed with sending your Bybit API and secret key.")

def handle_api_keys(update: Update, context: CallbackContext):
    # Handle API and secret key input from the user
    user_input = update.message.text
    if "API key" in user_input and "Secret Key" in user_input:
        update.message.reply_text("API keys received! You can now start trading.")
    else:
        update.message.reply_text("Please provide both API key and Secret Key.")

