# verification.py
import pytesseract
from PIL import Image
import mysql.connector

def extract_name_from_passport(image_path):
    """Extracts name from a passport image using OCR."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)

    # Simple logic to extract name from passport (adjust as per passport layout)
    for line in text.split("\n"):
        if "Name" in line:
            return line.split(":")[1].strip()
    return None

def check_duplicate(api_key, passport_name, db_connection):
    """Checks if API key or passport name already exists in the database."""
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users WHERE api_key = %s OR passport_name = %s", (api_key, passport_name))
    result = cursor.fetchone()
    if result:
        return True  # Duplicate found
    return False

def verify_user_passport_and_api(api_key, passport_image_path, db_connection):
    """Verifies the passport name matches and checks for duplicate registrations."""
    passport_name = extract_name_from_passport(passport_image_path)
    
    if passport_name:
        if check_duplicate(api_key, passport_name, db_connection):
            return "Duplicate registration detected."

        # Save details to database (name, API key, etc.)
        # Example SQL (use prepared statements to avoid SQL injection)
        cursor = db_connection.cursor()
        cursor.execute("INSERT INTO users (passport_name, api_key) VALUES (%s, %s)", (passport_name, api_key))
        db_connection.commit()

        return "Verification successful. You are now registered."
    else:
        return "Could not extract name from passport. Please try again."
