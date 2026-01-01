import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

import admin_handlers
import report_handlers
import leave_handlers
from config import TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)

def create_application():
    """
    Creates and configures the Telegram Application.
    Standard PTB v20+ (sync)
    """

    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # ===== Commands =====
    application.add_handler(CommandHandler("start", admin_handlers.start_command))
    application.add_handler(CommandHandler("report", report_handlers.start_report))
    application.add_handler(CommandHandler("leave", leave_handlers.start_leave))
    application.add_handler(CommandHandler("myreports", report_handlers.show_my_reports))
    application.add_handler(CommandHandler("myleaves", leave_handlers.show_my_leaves))

    # ===== Conversations (must be before menu text handler) =====
    application.add_handler(report_handlers.report_conversation)
    application.add_handler(leave_handlers.leave_conversation)

    # ===== Callback Queries =====
    application.add_handler(
        CallbackQueryHandler(
            report_handlers.handle_callbacks,
            pattern="^(confirm_report|cancel_report)$"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            leave_handlers.handle_callbacks,
            pattern="^(leave_|confirm_leave|cancel_leave)$"
        )
    )

    # ===== Menu text handler (LIMITED) =====
    application.add_handler(
        MessageHandler(
            filters.Regex("^(📝 گزارش جدید|📊 گزارش‌های من|🏖️ درخواست مرخصی|📂 مرخصی‌های من)$"),
            admin_handlers.handle_text_menu
        )
    )

    logger.info("✅ Application handlers registered.")
    return application
