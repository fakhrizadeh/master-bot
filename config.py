import os

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN is not set in environment variables")

# Admin / User IDs
YOUR_USER_ID = int(os.getenv("YOUR_USER_ID", "63614689"))
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "63614689"))

# Forum / Threads
FORUM_CHAT_ID = -1002891150464
TARGET_MESSAGE_THREAD_ID = 7
LEAVE_REQUEST_THREAD_ID = 5

# Time / Scheduler
TEHRAN_TIMEZONE_STR = "Asia/Tehran"
REPORT_REMINDER_TIME_MORNING = 9
REPORT_REMINDER_TIME_EVENING = 18
