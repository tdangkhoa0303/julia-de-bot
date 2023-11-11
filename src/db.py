from pymongo import MongoClient

client = MongoClient("mongodb://julia:julia@localhost:2104")

db = client['julia-de-bot']

Conversations = db['conversations']
