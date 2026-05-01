import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["resumes"]

resumes_collection = db["resumes"]
users_collection = db["users"]
