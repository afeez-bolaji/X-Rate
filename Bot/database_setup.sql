CREATE DATABASE IF NOT EXISTS xrate_bot;

USE xrate_bot;

-- Create users table to store user information
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    telegram_user_id BIGINT NOT NULL UNIQUE,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    passport_image_path VARCHAR(255),
    api_key VARCHAR(255),
    api_secret VARCHAR(255),
    bybit_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Ensure that API keys and user Telegram IDs are unique
CREATE UNIQUE INDEX idx_telegram_user_id ON users (telegram_user_id);
CREATE UNIQUE INDEX idx_api_key ON users (api_key);
