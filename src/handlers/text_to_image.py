from telegram import Update
from telegram.ext import ContextTypes
from io import BytesIO

from ..query_client import api_post

API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

def predict_reply(prompt):
  response = api_post(
    API_URL, 
    {
      "inputs": prompt,
    }
  )
  
  return response.content

async def text_to_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  message = update.message.text
  image_bytes = predict_reply(message)
  try:
    image_io = BytesIO(image_bytes)
    await update.message.reply_photo(image_io)
  except:
    print("Error:", image_bytes)
    await update.message.reply_text('Sorry, I cannot generate an image for you. Please try to rephrase your prompt.')
