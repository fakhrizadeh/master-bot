@echo off
title Daily Report Telegram Bot
echo ================================
echo Starting Telegram Bot...
echo ================================

REM ===== Set Environment Variables =====
set TELEGRAM_BOT_TOKEN=PUT_YOUR_BOT_TOKEN_HERE
set YOUR_USER_ID=63614689
set ADMIN_CHAT_ID=63614689

REM ===== Activate venv if exists =====
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

REM ===== Run bot =====
python main_bot.py

pause
