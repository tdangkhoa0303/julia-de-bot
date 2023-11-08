from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, ContextTypes
from models.user_data import UserData, ConversationRole
from models.chat_mode import ChatMode
from constants import TYPING_REPLY, CHOOSING, RECEIVING_PHOTO
from handlers.chat import chat_handler


CHAT_MODE_TEXT = {
  ChatMode.CHATTING: 'Chatting',
  ChatMode.GENDER_CLASSIFICATION: 'Gender Classification',
  ChatMode.GOOD_BYE: 'Good bye!'
}

CHAT_MODE_OPTIONS = [
  [CHAT_MODE_TEXT[ChatMode.CHATTING]],
  [CHAT_MODE_TEXT[ChatMode.GENDER_CLASSIFICATION]],
  [CHAT_MODE_TEXT[ChatMode.GOOD_BYE]],
]

# Define a dictionary to store user-specific data
user_data_dict: dict[str, UserData] = {}

INITIAL_CHATTING_MESSAGE = {
  "role": ConversationRole.SYSTEM,
  "content": "You are a friendly assistant who always responds in the style of a pirate",
}

markup = ReplyKeyboardMarkup(CHAT_MODE_OPTIONS, one_time_keyboard=True)

# Define functions for each state
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    # Initialize user-specific data
    user_data_dict[user.id] = UserData(user)
    
    await update.message.reply_text(
        f"Hello {user.first_name}! I'm your chatbot. How can I help you.",
        reply_markup=markup,
    )
    
    return CHOOSING
  
async def choose_chat_mode(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  user = update.message.from_user
  user_choice = update.message.text
  current_user = user_data_dict[user.id]
  selected_mode = next((key for key, value in CHAT_MODE_TEXT.items() if value == user_choice), None)
  context.user_data["selected_mode"] = selected_mode
  reply_content = 'Hello there, welcome to the Earth...'
  
  if selected_mode == ChatMode.CHATTING:
    current_user.select_mode(selected_mode)
    current_user.append_conversations(INITIAL_CHATTING_MESSAGE)
    reply_content = 'Greetings, Earthling! I come in peace and humor. Ready for a cosmic conversation?'
  elif selected_mode == ChatMode.GENDER_CLASSIFICATION:
    reply_content = "Hello! I'm here to assist with gender classification. Feel free to ask me any questions or provide information for analysis."
  
  await update.message.reply_text(reply_content)

  return TYPING_REPLY

async def typing_reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  message = update.message.text
  user = update.message.from_user
  current_user = user_data_dict[user.id]
  selected_mode = context.user_data["selected_mode"]
  
  if selected_mode == ChatMode.CHATTING:
    current_user.append_conversations({
      'role': ConversationRole.USER,
      'content': message
    })
    return chat_handler.call(current_user) 
  elif selected_mode == ChatMode.GENDER_CLASSIFICATION:
    reply_content = "Hello! I'm here to assist with gender classification. Feel free to ask me any questions or provide information for analysis."
  
  await update.message.reply_text(reply_content)
  

def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
  user_id = update.message.from_user.id
  photo_file = update.message.photo[-1].file_id
  user_data_dict[user_id]['photo'] = photo_file
  update.message.reply_text("Got it! Now, type something else.")
  return TYPING_REPLY


def main():
  # Create an Updater and pass it your bot's token
  application = ApplicationBuilder().token('6984320493:AAH46nXPWocYTSkZqa3sqajM9ZlqUagybdE').build()

  # Define the ConversationHandler with states and transitions
  conv_handler = ConversationHandler(
      entry_points=[CommandHandler('start', start)],
      states={
          RECEIVING_PHOTO: [MessageHandler(filters.PHOTO, receive_photo)],
          CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_chat_mode)],
          TYPING_REPLY: [
              MessageHandler(
                  filters.TEXT & ~filters.COMMAND,
                  typing_reply,
              )
          ],
      },
      fallbacks=[CommandHandler('cancel', cancel)],
      per_user=True,  # Make the handler per-user to handle multiple users
  )

  # Register the ConversationHandler
  application.add_handler(conv_handler)

  # Start the Bot
  application.run_polling()

  # Run the bot until you send a signal to stop it (e.g., with Ctrl+C)
  application.idle()

if __name__ == '__main__':
  main()
