import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise Exception("MONGO_URI is missing")

client = MongoClient(MONGO_URI)

db = client["resumes"]
jobdesc_collection = db["job_descriptions"]
users_collection = db["users"]
resumes_collection = db["resumes"]