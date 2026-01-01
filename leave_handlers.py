import logging
from telegram import (
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

import data_manager

logger = logging.getLogger(__name__)

# =======================
# States
# =======================
SELECT_TYPE, INPUT_DATE, CONFIRM = range(3)

# =======================
# /leave command
# =======================
async def start_leave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("🏖 روزانه", callback_data="leave_daily")],
            [InlineKeyboardButton("⏱ ساعتی", callback_data="leave_hourly")],
        ]
    )
    await update.message.reply_text("نوع مرخصی را انتخاب کنید:", reply_markup=kb)
    return SELECT_TYPE


# =======================
# انتخاب نوع مرخصی
# =======================
async def select_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    context.user_data["leave_type"] = query.data.replace("leave_", "")
    await query.edit_message_text("📅 تاریخ مرخصی را وارد کنید (YYYY-MM-DD):")
    return INPUT_DATE


# =======================
# وارد کردن تاریخ
# =======================
async def input_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.message.text == "❌ لغو":
        return await cancel_leave(update, context)

    context.user_data["date"] = update.message.text

    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ تایید", callback_data="confirm_leave")],
            [InlineKeyboardButton("❌ لغو", callback_data="cancel_leave")],
        ]
    )
    await update.message.reply_text(
        f"📄 خلاصه درخواست:\n"
        f"نوع: {context.user_data['leave_type']}\n"
        f"تاریخ: {context.user_data['date']}",
        reply_markup=kb,
    )
    return CONFIRM


# =======================
# تایید درخواست مرخصی
# =======================
async def confirm_leave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    data_manager.add_leave_request(
        user_id=query.from_user.id,
        leave_type=context.user_data["leave_type"],
        start_date=context.user_data["date"],
        end_date=None,
        comment=None,
    )

    await query.edit_message_text("✅ درخواست مرخصی ثبت شد.")
    context.user_data.clear()
    return ConversationHandler.END


# =======================
# لغو درخواست مرخصی
# =======================
async def cancel_leave(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.callback_query:
        await update.callback_query.edit_message_text("❌ لغو شد.")
    else:
        await update.message.reply_text("❌ لغو شد.")
    context.user_data.clear()
    return ConversationHandler.END


# =======================
# نمایش درخواست‌های مرخصی کاربر
# =======================
async def show_my_leaves(update: Update, context: ContextTypes.DEFAULT_TYPE):
    leaves = data_manager.get_user_leaves(update.effective_user.id)

    if not leaves:
        await update.message.reply_text("📭 درخواستی ثبت نشده است.")
        return

    for l in leaves:
        await update.message.reply_text(
            f"🏖 {l['leave_type']} | {l['start_date']} | وضعیت: {l['status']}"
        )


# =======================
# Callback handler
# =======================
async def handle_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("leave_"):
        return await select_type(update, context)

    if query.data == "confirm_leave":
        return await confirm_leave(update, context)

    if query.data == "cancel_leave":
        return await cancel_leave(update, context)


# =======================
# ConversationHandler
# =======================
leave_conversation = ConversationHandler(
    entry_points=[CommandHandler("leave", start_leave)],
    states={
        SELECT_TYPE: [CallbackQueryHandler(handle_callbacks)],
        INPUT_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, input_date)],
        CONFIRM: [CallbackQueryHandler(handle_callbacks)],
    },
    fallbacks=[CommandHandler("cancel", cancel_leave)],
)
