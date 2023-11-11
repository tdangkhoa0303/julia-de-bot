from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  await update.message.reply_text("Hey there! Thanks for choosing with me. If you ever fancy another chat or have questions, feel free to drop by. Take care and goodbye for now!")
  return ConversationHandler.END
