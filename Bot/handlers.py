from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from verification import verify_user_passport_and_api
import mysql.connector
import os

# Database connection function (for reuse)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

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
    """Handles the passport photo upload."""
    # Download the photo from Telegram
    photo = update.message.photo[-1]  # Get the highest quality photo
    file = await context.bot.get_file(photo.file_id)
    file_path = f"passport_{update.effective_user.id}.jpg"  # Save with user-specific filename
    await file.download(file_path)

    # Save the file path in the context for future use
    context.user_data["passport_image_path"] = file_path
    await update.message.reply_text("Passport photo received! Now please provide your Bybit API Key and Secret.")

async def handle_api_keys(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles API key submission and verification."""
    # Retrieve passport image path and API key from user input
    passport_image_path = context.user_data.get("passport_image_path")
    api_key = update.message.text

    if not passport_image_path:
        await update.message.reply_text("Please upload your passport photo first.")
        return

    # Database connection
    db_connection = get_db_connection()

    # Call verification logic (this checks passport, API key, and prevents duplicate entries)
    result = verify_user_passport_and_api(api_key, passport_image_path, db_connection)

    # Send the result of the verification process to the user
    await update.message.reply_text(result)

    # Close the database connection
    db_connection.close()

async def terms_and_policy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the terms and policy."""
    policy_text = "Terms and policy of using this bot: [Your terms here]"
    await update.message.reply_text(policy_text)
