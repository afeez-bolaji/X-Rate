# Configuration settings (e.g., API tokens)

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Access bot token from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
