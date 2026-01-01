import logging
from telegram import Bot
from config import ADMIN_CHAT_ID, YOUR_USER_ID

logger = logging.getLogger(__name__)

async def send_message_to_admin(bot: Bot, text: str, admin_id: int | None = None):
    """
    Send a message to the admin.
    """
    target = admin_id or ADMIN_CHAT_ID
    try:
        await bot.send_message(chat_id=target, text=text)
    except Exception as e:
        logger.error(f"Failed to send admin message: {e}")

def is_main_admin(user_id: int) -> bool:
    """
    Check if the user is the main admin.
    """
    return user_id == YOUR_USER_ID
