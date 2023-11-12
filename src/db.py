from pymongo import MongoClient

from .configs import ENV

client = MongoClient(ENV['MONGO_URI'])

db = client['julia-de-bot']

Conversations = db['conversations']
