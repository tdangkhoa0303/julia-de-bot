from telegram import Update, constants
from telegram.ext import ContextTypes
from transformers import AutoTokenizer

from ..builders.message_builder import MessageBuilder
from ..constants import CHOOSING, ASSISTANT_TOKEN, ChatMode
from ..db import Conversations
from ..query_client import api_post
from .text_to_image import text_to_image

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/zephyr-7b-beta")

def predict_reply(prompt):
  response = api_post(
    API_URL, 
    {
      "inputs": prompt,
      "parameters": {
        "max_new_tokens": 250,
        "temperature": 0.5,
        "top_k": 50,
        "top_p":0.8
      }
    }
  )

  return response.json()

def extract_predicted_response(outputs):
  generated_text = outputs[0]["generated_text"]
  return generated_text.split(ASSISTANT_TOKEN)[-1].strip()

async def reply_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  await context.bot.send_chat_action(
    chat_id=update.effective_message.chat_id, 
    action=constants.ChatAction.TYPING
  )
  
  message = update.message.text
  user = update.message.from_user
  conversation = Conversations.find_one({"user_id": user.id})
  if conversation is None:
    await update.message.reply_text("Please choose a mode first.")
    return CHOOSING
  
  reply_content = ""
  selected_mode = conversation['mode']
  
  if selected_mode == ChatMode.CHATTING:
    user_message = MessageBuilder().from_user(message).to_dict()
    Conversations.update_one(
      {"_id": conversation['_id']},
      {"$push": {
        "messages": user_message
      }}
    )
    previous_messages = conversation['messages']
    prompt = tokenizer.apply_chat_template(
      previous_messages + [user_message], 
      tokenize=False, 
      add_generation_prompt=True
    )
    
    reply = predict_reply(prompt)
    
    reply_content = extract_predicted_response(reply)
    Conversations.update_one(
      {"_id": conversation['_id']},
      {"$push": {
        "messages": MessageBuilder().from_assistant(reply_content).to_dict()
      }}
    )
    
    try:
      await update.message.reply_markdown_v2(reply_content)
    except:
      print("Error:", reply_content)
      await update.message.reply_text(reply_content)

  elif selected_mode == ChatMode.TEXT_TO_IMAGE:
    return await text_to_image(update, context)
