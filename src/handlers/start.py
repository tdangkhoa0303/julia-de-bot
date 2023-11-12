from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from ..constants import CHAT_MODE_TEXT, CHOOSING, ChatMode


CHAT_MODE_OPTIONS = [
  [CHAT_MODE_TEXT[ChatMode.CHATTING]],
  [CHAT_MODE_TEXT[ChatMode.TEXT_TO_IMAGE]],
]

markup = ReplyKeyboardMarkup(CHAT_MODE_OPTIONS, one_time_keyboard=True)

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
  user = update.message.from_user
  
  await update.message.reply_text(
      f"Hello {user.first_name}! I'm your chatbot. How can I help you.",
      reply_markup=markup,
  )
  
  return CHOOSING


