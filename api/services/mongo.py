from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI","mongodb://mongo:27017"))
db = client[os.getenv("MONGO_DB","cti")]
