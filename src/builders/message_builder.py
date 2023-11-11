from ..entities.message import Message, MessageRole

class MessageBuilder:
  def from_user(self, content: str):
    return Message(MessageRole.USER, content)
  
  def from_system(self, content: str):
    return Message(MessageRole.SYSTEM, content)
  
  def from_assistant(self, content: str):
    return Message(MessageRole.ASSISTANT, content)
