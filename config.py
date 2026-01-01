import os

# دریافت توکن ربات تلگرام از متغیر محیطی
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# چک کردن اگر توکن تلگرام وجود نداشت و ارور دادن
if not TELEGRAM_BOT_TOKEN:
    raise RuntimeError("❌ TELEGRAM_BOT_TOKEN is not set in environment variables")

# شناسه ادمین تلگرام (برای ارسال پیام‌ها به ادمین)
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "your-admin-chat-id"))

# در صورتی که از متغیر محیطی `ADMIN_CHAT_ID` استفاده می‌کنید، باید مقدار آن را در تنظیمات محیطی لیارا وارد کنید.
