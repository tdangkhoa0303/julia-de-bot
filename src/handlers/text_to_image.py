from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from io import BytesIO

from ..constants import ChatMode, VotingOption
from ..db import Conversations
from ..builders.message_builder import MessageBuilder
from ..query_client import api_post
from .guarantee_user_available import guarantee_user_available

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

def predict_reply(prompt):
  response = api_post(
    API_URL, 
    {
      "inputs": prompt,
    }
  )
  
  return response.content

markup = ReplyKeyboardMarkup([[VotingOption.NO]], one_time_keyboard=True)

async def text_to_image(update: Update, context: ContextTypes.DEFAULT_TYPE, custom_message = None) -> int:
  await guarantee_user_available(update)
  args = context.args
  if not args and not custom_message:
    await update.message.reply_text('Sorry, please provide some descriptions that you want to include in your desired image.')
    return
  
  user_prompt = custom_message or ' '.join(args)
  user = update.message.from_user
  
  user_message = MessageBuilder().from_user(user_prompt).to_dict()
  Conversations.update_one(
    {"user_id": user.id},
    {
      "$push": {
        "messages": user_message
      },
      "$set": {
        "previous_prompt": {
          "mode": ChatMode.TEXT_TO_IMAGE,
          "message": user_message
        }
      }
    }
  )
  
  image_bytes = predict_reply(user_prompt)
  try:
    image_io = BytesIO(image_bytes)
    await update.message.reply_photo(image_io)
    Conversations.update_one(
      {"user_id": user.id},
      {"$push": {
        "messages": MessageBuilder().from_assistant(f"Generated image for {user_message}").to_dict()
      }}
    )
  except Exception as error:
    print("Error:", error)
    error_message = "Sorry, I cannot generate an image for you. Please try to rephrase your prompt."
    await update.message.reply_text(error_message)
    Conversations.update_one(
      {"user_id": user.id},
      {"$push": {
        "messages": MessageBuilder().from_assistant(error_message).to_dict()
      }}
    )
