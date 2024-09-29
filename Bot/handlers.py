from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a greeting message and prompts the user to sign up for Bybit."""
    user = update.effective_user
    welcome_message = f"Hello {user.first_name}! Welcome to our bot. Please sign up on Bybit to use our services."
    await update.message.reply_text(welcome_message)

    # Instructions and Bybit registration link
    description = (
        "To get started with P2P trading, please sign up on Bybit.\n"
        "1. Click the link below to register.\n"
        "2. Complete the KYC verification.\n"
        "3. Generate and send your API Key and Secret to this bot."
    )
    keyboard = [[InlineKeyboardButton("Sign up for Bybit", url="https://www.bybit.com/en/register")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(description, reply_markup=reply_markup)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the photo upload."""
    await update.message.reply_text("Photo received! Please upload your passport photo as well.")

async def handle_api_keys(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles API key submission."""
    await update.message.reply_text("Please provide your Bybit API Key and Secret.")

async def terms_and_policy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the terms and policy."""
    policy_text = "Terms and policy of using this bot: [Your terms here]"
    await update.message.reply_text(policy_text)
