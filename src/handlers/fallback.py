from telegram import Update
from telegram.ext import ContextTypes

from ..constants import CHOOSING, ChatMode
from ..db import Conversations
from .reply_chat import reply_chat

async def fallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  user = update.message.from_user
  conversation = Conversations.find_one({"user_id": user.id})
    
  if conversation is not None:
    return await reply_chat(update, context)
  
  await update.message.reply_text("Please choose a mode first.")
  return CHOOSING
