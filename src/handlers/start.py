from telegram import Update

from telegram.ext import ContextTypes
from ..builders.message_builder import MessageBuilder
from ..db import Conversations
from ..constants import DEFAULT_RESPONSE
from .guarantee_user_available import guarantee_user_available

INITIAL_CHATTING_MESSAGE = MessageBuilder().from_system('''
                                                        You are Julia - a friendly assistant that always try to help user resolve user's problem.
                                                        You can use markdown and emoji to response to the user. Your response MUST BE IN FIRST PERSON.
                                                        ''').to_dict()

async def upsert_conversation(user_id: int, payload: dict[str, any]):
  conversation = Conversations.find_one({"user_id": user_id})
  if conversation is not None:
    return Conversations.update_many(
      {"_id": conversation['_id']},
      {"$set": payload}
    ) 
  
  return Conversations.insert_one({
      'user_id': user_id,
      **payload
    })
  
async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
  await guarantee_user_available(update, reinitialize=True)
  
  await update.message.reply_markdown_v2(DEFAULT_RESPONSE)


