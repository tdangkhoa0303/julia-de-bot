from enum import Enum
from .helpers import escape_markdown


ASSISTANT_TOKEN = '<|assistant|>'

class ChatMode(str, Enum):
  CHATTING = 'chatting',
  TEXT_TO_IMAGE = 'text_to_image',
  
  def __repr__(self):
      return self.value

CHAT_MODE_TEXT = {
  ChatMode.CHATTING: 'Chat',
  ChatMode.TEXT_TO_IMAGE: 'Text To Image',
}
class VotingOption(str, Enum):
  YES = 'Awesome',
  NO = '/regenerate',
  
  def __repr__(self):
      return self.value

DEFAULT_RESPONSE = escape_markdown("""
👋 Hello there! I'm Julia, your friendly chatbot companion. Whether you have questions, need assistance, or just fancy a chat, I'm here for you! Feel free to ask me anything, and let's explore the world of knowledge together. How can I assist you today? 🤖✨

Here are some useful command you can play with me:
- `/start` - Let's have a chat.
- `/genimg [prompt]` - Give me a description and I will generate an image for you.
- `/regenerate` - Regenerate your previous prompt if my answer is not satisfied you.
- `/help` - Show this message.
- `/bye` - Say goodbye to me.
""")
