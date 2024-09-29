# Inline and reply keyboards

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def bybit_registration_keyboard():
    # Inline keyboard with Bybit registration link
    keyboard = [
        [InlineKeyboardButton("Register on Bybit", url="https://www.bybit.com/en/register")]
    ]
    return InlineKeyboardMarkup(keyboard)
