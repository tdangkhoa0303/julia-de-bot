from telegram import Update, constants
from telegram.ext import ContextTypes

from .text_to_image import text_to_image
from .reply_chat import reply_chat
from ..db import Conversations
from ..constants import ChatMode
  
async def regenerate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  await context.bot.send_chat_action(
    chat_id=update.effective_message.chat_id, 
    action=constants.ChatAction.TYPING
  )
  
  user = update.message.from_user
  reply_content = 'Greetings, Earthling! I come in peace and humor. Ready for a cosmic conversation?'
  conversation = Conversations.find_one({"user_id": user.id})
  if conversation is None or conversation['previous_prompt'] is None:
    await update.message.reply_text(reply_content)
  
  previous_messages = conversation['messages']
  previous_prompt = conversation['previous_prompt']
  previous_mode = previous_prompt['mode']
  
  Conversations.update_one(
    {"_id": conversation['_id']},
    {
      "$set": {
        "messages": previous_messages[:-1]
      }
    }
  )
  
  if previous_mode == ChatMode.CHATTING:
    await reply_chat(update, context)
  elif previous_mode == ChatMode.TEXT_TO_IMAGE:
    await text_to_image(update, context, custom_message=previous_prompt['message']['content'])
  else: 
    await update.message.reply_text(reply_content) 
