from enum import Enum

# Define states for the conversation
CHOOSING, TYPING_REPLY = range(2)

ASSISTANT_TOKEN = '<|assistant|>'

class ChatMode(str, Enum):
  CHATTING = 'chatting',
  TEXT_TO_IMAGE = 'text_to_image',
  GOOD_BYE = 'good_bye'
  
  def __repr__(self):
      return self.value

CHAT_MODE_TEXT = {
  ChatMode.CHATTING: 'Chat',
  ChatMode.TEXT_TO_IMAGE: 'Text To Image',
  ChatMode.GOOD_BYE: 'Good bye!'
}
