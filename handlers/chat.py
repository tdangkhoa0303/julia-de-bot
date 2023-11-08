import torch
from transformers import pipeline

from models.user_data import UserData, ConversationRole
    
pipe = pipeline("text-generation", model="HuggingFaceH4/zephyr-7b-beta", torch_dtype=torch.bfloat16, device_map="auto")

    
class ChatHandler:
  def __init__(self) -> None:
    pass
  
  def call(self, userData: UserData) -> int:
    conversations = userData.conversations
    prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
    print(outputs[0]["generated_text"])
  
  
chat_handler = ChatHandler()