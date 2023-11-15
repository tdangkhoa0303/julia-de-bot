from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

from ..db import Conversations

async def bye(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  await update.message.reply_text(
    "👋 It was a pleasure chatting with you! If you ever have more questions or just want to have a friendly chat, feel free to reach out. Until next time, take care and have a wonderful day! Goodbye! 👋🌟",
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
