from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from ..db import Conversations

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  await update.message.reply_text(
    "Hey there! Thanks for choosing with me. If you ever fancy another chat or have questions, feel free to drop by. Take care and goodbye for now!",
    reply_markup=ReplyKeyboardRemove(),
  )
  
  user = update.message.from_user
  conversation = Conversations.find_one({"user_id": user.id})
  if conversation is not None:
    Conversations.update_many(
      {"_id": conversation['_id']},
      {
        "$set": {"mode": None, "messages": []},
      }
    ) 
  
  return ConversationHandler.END
