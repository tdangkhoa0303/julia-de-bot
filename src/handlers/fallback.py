from telegram import Update
from telegram.ext import ContextTypes

from ..constants import DEFAULT_RESPONSE

async def fallback(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
  await update.message.reply_markdown_v2(DEFAULT_RESPONSE)
