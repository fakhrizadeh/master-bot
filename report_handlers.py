import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)

# ==========================
# States
# ==========================
INPUT_PERFORMANCE, CONFIRM_PERFORMANCE = range(2)

# ==========================
# ارسال پیام خودکار هر روز ساعت 9 صبح
# ==========================
async def send_daily_report_prompt(context: ContextTypes.DEFAULT_TYPE):
    """
    ارسال پیام به کاربران هر روز ساعت 9 صبح به وقت تهران.
    """
    tehran_tz = pytz.timezone("Asia/Tehran")
    current_time = datetime.now(tehran_tz)
    formatted_date = current_time.strftime("%A %Y/%m/%d")  # فرمت تاریخ شمسی و روز هفته
    message = f"لطفاً عملکرد روزانه خود (نام روز هفته و تاریخ روز بصورت تاریخ شمسی) را ارسال کنید.\n"

    # ارسال به همه کاربران یا یک کاربر خاص
    await context.bot.send_message(
        chat_id="YOUR_CHAT_ID",  # شناسه چت کاربر یا گروه
        text=message
    )


# ==========================
# هندلر دکمه "ارسال عملکرد"
# ==========================
async def start_daily_performance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    دریافت عملکرد روزانه از کاربر.
    """
    await update.message.reply_text(
        "لطفاً عملکرد امروز خود را ارسال کنید.\nهر تسک را در یک ردیف بنویسید."
    )
    return INPUT_PERFORMANCE  # تغییر حالت برای تایید و دریافت اطلاعات

async def receive_performance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    دریافت متن عملکرد روزانه از کاربر.
    """
    text = update.message.text
    user = update.effective_user
    today = datetime.now(pytz.timezone("Asia/Tehran"))
    formatted_date = today.strftime("%Y/%m/%d")  # تاریخ شمسی
    day_of_week = today.strftime("%A")  # نام روز هفته

    # فرمت کردن گزارش
    formatted_performance = f"عملکرد {day_of_week} {formatted_date}\n"
    tasks = text.split("\n")
    for idx, task in enumerate(tasks):
        formatted_performance += f"{idx + 1}. {task.strip()}\n"

    # اضافه کردن اطلاعات کاربر
    formatted_performance += f"\n-------------------------------\n"
    formatted_performance += f"نام: {user.full_name} #{user.username}\n"
    formatted_performance += f"تاریخ و زمان ارسال: {today.strftime('%Y/%m/%d %H:%M:%S')}\n"

    # نمایش پیش‌نمایش و تایید
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ تایید", callback_data="confirm_performance")],
            [InlineKeyboardButton("❌ لغو", callback_data="cancel_performance")]
        ]
    )

    await update.message.reply_text(
        f"📄 *پیش‌نمایش عملکرد شما:*\n\n{formatted_performance}",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )
    context.user_data["formatted_performance"] = formatted_performance
    return CONFIRM_PERFORMANCE  # تغییر حالت تایید

async def confirm_performance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    تایید عملکرد روزانه و ذخیره آن.
    """
    query = update.callback_query
    await query.answer()

    # ذخیره عملکرد
    performance_data = context.user_data["formatted_performance"]
    user_id = update.effective_user.id
    # ذخیره عملکرد در دیتابیس یا فایل (در اینجا نمایش داده می‌شود)
    logger.info(f"Performance saved for user {user_id}: {performance_data}")

    await query.edit_message_text("✅ عملکرد با موفقیت ثبت شد.")
    await query.message.reply_text(
        "⬅️ به منوی اصلی برگشتید."
    )
    context.user_data.clear()
    return ConversationHandler.END  # پایان فرآیند

async def cancel_performance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    لغو عملکرد روزانه.
    """
    if update.callback_query:
        await update.callback_query.edit_message_text("❌ ارسال عملکرد لغو شد.")
    else:
        await update.message.reply_text("❌ ارسال عملکرد لغو شد.")

    context.user_data.clear()
    return ConversationHandler.END  # پایان فرآیند


# ==========================
# هندلر دکمه "گزارش‌گیری از عملکردها"
# ==========================
async def show_performance_reports(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    نمایش گزارش‌های عملکرد قبلی کاربر.
    """
    user_id = update.effective_user.id
    # اینجا باید داده‌های گزارش‌ها از فایل یا دیتابیس خوانده شوند
    performances = context.user_data.get("performances", [])
    
    if not performances:
        await update.message.reply_text("📭 شما هیچ گزارشی ارسال نکرده‌اید.")
        return

    # ارسال گزارش‌ها به صورت صفحه‌بندی شده یا با فرمت مناسب
    for performance in performances:
        await update.message.reply_text(performance, parse_mode="Markdown")
    await update.message.reply_text("⬅️ به منوی اصلی برگشتید.")


# ==========================
# افزودن هندلرها به ربات
# ==========================
def add_handlers(application):
    application.add_handler(CallbackQueryHandler(show_performance_reports, pattern="^show_performance_reports$"))
    application.add_handler(CallbackQueryHandler(confirm_performance, pattern="^confirm_performance$"))
    application.add_handler(CallbackQueryHandler(cancel_performance, pattern="^cancel_performance$"))
    application.add_handler(ConversationHandler(
        entry_points=[CommandHandler("daily_performance", start_daily_performance)],
        states={
            INPUT_PERFORMANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_performance)],
            CONFIRM_PERFORMANCE: [CallbackQueryHandler(handle_callbacks)],
        },
        fallbacks=[CommandHandler("cancel", cancel_performance)],
    ))
