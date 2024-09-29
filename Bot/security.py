# Security functions (e.g., environment variable loading)

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to get environment variable
def get_env_var(variable_name):
    return os.getenv(variable_name)
