from datetime import datetime
from enum import Enum

class MessageRole(str, Enum):
  SYSTEM = 'system'
  USER = 'user'
  ASSISTANT = 'assistant'
  
  def __repr__(self):
      return self.value

class Message:
  def __init__(self, role: str, content: str):
    self.role = role
    self.content = content
    self.created = datetime.now()
    
  def to_dict(self):
    return vars(self)


