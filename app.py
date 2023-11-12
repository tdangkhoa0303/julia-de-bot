from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler

from src.constants import TYPING_REPLY, CHOOSING
from src.handlers.fallback import fallback
from src.handlers.choose_mode import choose_mode
from src.handlers.reply_chat import reply_chat
from src.handlers.start import start
from src.handlers.bye import bye
from src.configs import ENV

def main():
  # Create an Updater and pass it your bot's token
  application = ApplicationBuilder().token(ENV['TELEGRAM_BOT_TOKEN']).build()

  # Define the ConversationHandler with states and transitions
  conv_handler = ConversationHandler(
      entry_points=[
        CommandHandler('start', start), 
        MessageHandler(filters.ALL & ~filters.COMMAND, fallback),
        CommandHandler('bye', bye)
      ],
      states={
          CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_mode)],
          TYPING_REPLY: [
            MessageHandler(
              filters.TEXT & ~filters.COMMAND,
              reply_chat,
            )
          ],
      },
      fallbacks=[
        MessageHandler(filters.ALL & ~filters.COMMAND, fallback),
        CommandHandler('bye', bye), 
      ],
      per_user=True,
  )

  # Register the ConversationHandler
  application.add_handler(conv_handler)

  # Start the Bot
  application.run_polling()

  # Run the bot until you send a signal to stop it (e.g., with Ctrl+C)
  application.idle()

if __name__ == '__main__':
  main()
