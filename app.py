from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
import os

app = Flask(__name__)

# ✅ JWT secret key (must be set in Render)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
jwt = JWTManager(app)

# ✅ Allow requests from your Vercel frontend and local dev
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "https://fresume-henna.vercel.app"
]}}, supports_credentials=True)

# ✅ MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["resumes"]

users_collection = db["users"]
resumes_collection = db["resumes"]

# ---------------------------
# 🔹 Register Route
# ---------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        if users_collection.find_one({"username": username}):
            return jsonify({"error": "User already exists"}), 400

        hashed_pw = generate_password_hash(password)
        users_collection.insert_one({"username": username, "password": hashed_pw})
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        print("Register error:", e)
        return jsonify({"error": "Server error"}), 500

# ---------------------------
# 🔹 Login Route
# ---------------------------
@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        user = users_collection.find_one({"username": username})
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=username)
        return jsonify({"access_token": token}), 200
    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Server error"}), 500

# ---------------------------
# 🔹 Health Check
# ---------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})

# ---------------------------
# 🔹 Run App
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
