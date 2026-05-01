# import os
# from pymongo import MongoClient

# MONGO_URI = os.getenv("MONGO_URI")

# if not MONGO_URI:
#     raise Exception("MONGO_URI is missing")

# client = MongoClient(MONGO_URI)
# db = client["resumes"]

# resumes_collection = db["resumes"]
# users_collection = db["users"]

import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI is missing")

client = MongoClient(MONGO_URI)

db = client["resumes"]

users_collection = db["users"]
resumes_collection = db["resumes"]