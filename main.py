import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
import os
from config import TELEGRAM_BOT_TOKEN, ADMIN_CHAT_ID
from datetime import datetime
import pytz

# تنظیمات لاگ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ==============================
# ارسال پیغام به ادمین بعد از اتصال ربات
# ==============================
async def send_connection_message(context: ContextTypes.DEFAULT_TYPE):
    """
    ارسال پیغام موفقیت‌آمیز به ادمین ربات بعد از اتصال.
    """
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text="✅ ربات با موفقیت متصل شد و آماده به کار است!"
    )

# ==============================
# دستور /start برای تست اتصال
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    ارسال پیغام خوشامدگویی برای بررسی اتصال
    """
    await update.message.reply_text("👋 ربات با موفقیت به شما متصل شد!")

# ==============================
# ساخت و تنظیم ربات
# ==============================
def create_application():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # دستور /start
    application.add_handler(CommandHandler("start", start))

    # تنظیم زمان‌بندی برای ارسال پیغام اتصال به ادمین
    job_queue = application.job_queue
    job_queue.run_once(send_connection_message, when=0)

    return application

# ==============================
# راه‌اندازی ربات
# ==============================
def main():
    """
    ورود به ربات و راه‌اندازی آن
    """
    app = create_application()
    app.run_polling()

if __name__ == "__main__":
    main()
