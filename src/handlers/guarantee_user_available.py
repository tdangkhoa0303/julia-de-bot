from telegram import Update

from ..builders.message_builder import MessageBuilder
from ..db import Conversations

INITIAL_CHATTING_MESSAGE = MessageBuilder().from_system('''
                                                        You are Julia - a friendly assistant that always try to help user resolve user's problem.
                                                        You can use markdown and emoji to response to the user. Your response MUST BE IN FIRST PERSON.
                                                        ''').to_dict()

async def upsert_conversation(user_id: int, payload: dict[str, any], reinitialize = False):
  conversation = Conversations.find_one({"user_id": user_id})
  if conversation is None:
    return Conversations.insert_one({
      'user_id': user_id,
      **payload
    })
  
  if reinitialize:
    return Conversations.update_many(
      {"_id": conversation['_id']},
      {"$set": payload}
    ) 
    
  return conversation
  
  
async def guarantee_user_available(update: Update, reinitialize = False) -> int:
  user = update.message.from_user
  await upsert_conversation(
    user.id, 
    {
      'messages': [INITIAL_CHATTING_MESSAGE]
    }, 
    reinitialize
  )


