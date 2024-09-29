# Database connection and queries

import mysql.connector
import os
from bot.security import get_env_var

# Connect to MySQL Database
def get_db_connection():
    connection = mysql.connector.connect(
        host=get_env_var("DB_HOST"),
        user=get_env_var("DB_USER"),
        password=get_env_var("DB_PASSWORD"),
        database=get_env_var("DB_NAME")
    )
    return connection

# Save user API key and secret key to the database
def save_user_api_keys(user_id, api_key, secret_key):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, api_key, secret_key)
        VALUES (%s, %s, %s)
    """, (user_id, api_key, secret_key))
    conn.commit()
    cursor.close()
    conn.close()

