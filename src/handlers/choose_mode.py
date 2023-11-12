from telegram import Update, constants
from telegram.ext import ContextTypes

from ..builders.message_builder import MessageBuilder
from ..constants import CHAT_MODE_TEXT, TYPING_REPLY, ChatMode
from ..db import Conversations

INITIAL_CHATTING_MESSAGE = MessageBuilder().from_system('''
                                                        You are a friendly assistant that always try to help user resolve their coding problem. 
                                                        You can use markdown and emoji in your response.
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
  
async def choose_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  await context.bot.send_chat_action(
    chat_id=update.effective_message.chat_id, 
    action=constants.ChatAction.TYPING
  )
  
  user = update.message.from_user
  user_choice = update.message.text
  
  selected_mode = next((key for key, value in CHAT_MODE_TEXT.items() if value == user_choice), None)
  context.user_data["selected_mode"] = selected_mode
  reply_content = 'Hello there, welcome to the Earth...'
  
  messages = []
  if selected_mode == ChatMode.CHATTING:
    reply_content = 'Greetings, Earthling! I come in peace and humor. Ready for a cosmic conversation?'
    messages = [INITIAL_CHATTING_MESSAGE]
  elif selected_mode == ChatMode.TEXT_TO_IMAGE:
    reply_content = "Hello! I'm your text-to-image chatbot, ready to turn your words into visual wonders. What can I create for you today?"
  
  
  await upsert_conversation(user.id, {
    'mode': selected_mode,
    'messages': messages
  })
  
  await update.message.reply_text(reply_content)

  return TYPING_REPLY
