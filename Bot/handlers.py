from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from passport_validator import validate_passport
from verification import verify_user_passport_and_api
import mysql.connector
import requests


# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a greeting message and provides step-by-step instructions for signing up."""
    user = update.effective_user
    welcome_message = (
        f"Hello {user.first_name}! 👋\n\n"
        "Welcome to our bot, designed to help you get started with P2P trading.\n"
        "To begin, you'll need to complete the following steps:"
    )
    instructions = (
        "1️⃣ Sign up for Bybit using the link below.\n"
        "2️⃣ Complete the KYC (Know Your Customer) verification process.\n"
        "3️⃣ Upload your passport photo here for identity verification.\n"
        "4️⃣ Generate your API Key and Secret on Bybit and send them to this bot.\n"
        "\nOnce you've completed these steps, you'll be ready to trade! 🚀"
    )

    # Bybit registration link
    keyboard = [[InlineKeyboardButton("Sign up for Bybit", url="https://www.bybit.com/en/register")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send welcome message, instructions, and the registration link
    await update.message.reply_text(welcome_message)
    await update.message.reply_text(instructions, reply_markup=reply_markup)

    # Guide user to upload passport next
    await update.message.reply_text(
        "📷 Please upload your passport photo now for verification purposes. Use the 'Attach' button to send the photo."
    )



import traceback
import logging

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles passport photo upload."""
    
    try:
        photos = update.message.photo
        max_index = len(photos) - 1
        
        # Wait for the file to be retrieved from Telegram's servers
        file_info = await context.bot.get_file(photos[max_index].file_id)
        
        print("Retrieved file info successfully.")
        
        # Download the file content as a byte array
        file_content = await file_info.download_as_bytearray()
    
    except Exception as e:
    # Handle the exception more robustly
    
        logging.error(f"Error handling photo upload: {e}")
        
        try:
            # Send a friendly error message to the user
            print("Sending error message...")
            await update.message.reply_text("An error occurred while processing your passport image. Please try again.")
            
        except Exception as e2:
            print(traceback.format_exc())
    else:
        print("Processing file...")
        
        # Save the file content to a local file
        with open(f"passport_{update.effective_user.id}.jpg", 'wb') as f:
            f.write(file_content)
            
        context.user_data["passport_image_path"] = f"passport_{update.effective_user.id}.jpg"
        
        print("Saved file successfully.")
        
        # Use a try-except block to catch any exceptions
        try:
            await validate_passport(update, context)
            print("Validated passport successfully.")
            
        except Exception as e3:
            logging.error(f"Error validating passport: {e3}")








async def handle_api_keys(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles API key and secret submission."""
    # Retrieve the passport image path
    passport_image_path = context.user_data.get("passport_image_path")
    api_key = update.message.text

    # Ensure that the passport photo is uploaded first
    if not passport_image_path:
        await update.message.reply_text("⚠️ Please upload your passport photo before submitting your API keys.")
        return

    # Connect to the database and verify the user's API key and passport
    db_connection = get_db_connection()
    result = verify_user_passport_and_api(api_key, passport_image_path, db_connection)

    # Inform the user about the verification result
    await update.message.reply_text(result)

    # Close the database connection
    db_connection.close()

async def terms_and_policy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the bot's terms and conditions."""
    policy_text = (
        "📜 *Terms and Policy*\n\n"
        "By using this bot, you agree to the following:\n"
        "1. Your data will be used solely for the purpose of verification and API integration with Bybit.\n"
        "2. You are responsible for keeping your API Key and Secret secure.\n"
        "3. Unauthorized or fraudulent use will result in the termination of your access.\n"
        "\nFor more details, please refer to our full terms and conditions."
    )
    await update.message.reply_text(policy_text, parse_mode="Markdown")

