from enum import Enum
from models.chat_mode import ChatMode

class ConversationRole(Enum):
  SYSTEM = 'system'
  USER = 'user'
  ASISSTANT = 'assistant'

class UserData:
  def __init__(self, user):
    self.user = user
    self.conversations = []
    self.mode = None
    
  def append_conversations(self, role: ConversationRole, content: str): 
    self.conversation.append({
      "role": role,
      "content": content
    })
    
  def reset_conversations(self):
    self.conversations = []
    
  def select_mode(self, selected_mode: ChatMode):
    self.mode = selected_mode