from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from db import users_collection, resumes_collection
from model import rank_resumes, generate_analytics, extract_metadata

app = Flask(__name__)

# ✅ JWT secret key (must be set in Render)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

# 🔹 Explicitly set algorithm and expiry
from datetime import timedelta
app.config["JWT_ALGORITHM"] = "HS256"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # token valid for 1 hour

jwt = JWTManager(app)

# ✅ Allow requests from local dev and all Vercel preview domains
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:5173",
    "https://fresume-nine.vercel.app",
    "https://fresume-git-main-arman-mohamand-projects.vercel.app",
    "https://fresume-*.vercel.app"  # wildcard for previews
]}}, supports_credentials=True)

# ---------------------------
# 🔹 Register Route
# ---------------------------
@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        print("Register incoming data:", data)  # Debug log

        username = data.get("username")
        password = data.get("password")

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
        data = request.get_json()
        print("Login incoming data:", data)  # Debug log

        username = data.get("username")
        password = data.get("password")

        user = users_collection.find_one({"username": username})
        if not user or not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=username)
        return jsonify({"access_token": token}), 200
    except Exception as e:
        print("Login error:", e)
        return jsonify({"error": "Server error"}), 500

# ---------------------------
# 🔹 Upload Resume
# ---------------------------
@app.route("/upload", methods=["POST"])
@jwt_required()
def upload_resume():
    try:
        data = request.get_json()
        print("Upload incoming data:", data)  # Debug log

        filename = data.get("filename")
        text = data.get("text")

        if not filename or not text:
            return jsonify({"error": "Missing filename or text"}), 400

        metadata = extract_metadata(text)

        resumes_collection.insert_one({
            "filename": filename,
            "text": text,
            "metadata": metadata,
            "uploaded_at": datetime.utcnow()
        })

        return jsonify({"message": "Resume uploaded successfully"}), 201
    except Exception as e:
        print("Upload error:", e)
        return jsonify({"error": "Server error"}), 500

# ---------------------------
# 🔹 Rank Resumes
# ---------------------------
@app.route("/rank", methods=["POST"])
@jwt_required()
def rank():
    try:
        data = request.get_json()
        print("Rank incoming data:", data)  # Debug log

        skills = data.get("skills", [])
        job_desc = data.get("job_description", "")

        resumes_data = list(resumes_collection.find())
        resumes = [r["text"] for r in resumes_data]

        results = rank_resumes(resumes, job_desc, skills)
        for i, r in enumerate(results):
            r["metadata"] = resumes_data[i].get("metadata", {})

        analytics = generate_analytics(results, skills)

        return jsonify({
            "total_resumes": len(resumes),
            "results": results,
            "analytics": analytics
        })
    except Exception as e:
        print("Rank error:", e)
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
