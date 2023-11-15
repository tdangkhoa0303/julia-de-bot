from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler

from src.handlers.fallback import fallback
from src.handlers.regenerate import regenerate
from src.handlers.reply_chat import reply_chat
from src.handlers.start import start
from src.handlers.text_to_image import text_to_image
from src.handlers.bye import bye
from src.configs import ENV

def main():
  application = ApplicationBuilder().token(ENV['TELEGRAM_BOT_TOKEN']).build()
  
  conv_handler = ConversationHandler(
      entry_points=[
        CommandHandler('start', start),
        CommandHandler('genimg', text_to_image),
        CommandHandler('regenerate', regenerate),
        CommandHandler('bye', bye),
        CommandHandler('help', fallback),
        MessageHandler(
          filters.TEXT & ~filters.COMMAND,
          reply_chat,
        )
      ],
      states={},
      fallbacks=[
        CommandHandler('start', start),
        CommandHandler('regenerate', regenerate),
        CommandHandler('genimg', text_to_image),
        CommandHandler('bye', bye),
        CommandHandler('help', fallback),
        MessageHandler(
          filters.TEXT & ~filters.COMMAND,
          reply_chat,
        )
      ],
      per_user=True,
  )
  
  application.add_handler(conv_handler)
  
  application.run_polling()
  application.idle()

if __name__ == '__main__':
  main()
