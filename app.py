import os
import fitz  # PyMuPDF
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flasgger import Swagger
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from db import resumes_collection, users_collection
from model import rank_resumes, generate_analytics, extract_metadata

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # ⚠️ change in production
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=365)
jwt = JWTManager(app)
swagger = Swagger(app)
CORS(app, origins=["http://localhost:5173"])

UPLOAD_FOLDER = "resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_text(file_path):
    """Extract text from PDF resumes using PyMuPDF"""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ------------------ AUTH ------------------

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    users_collection.insert_one({"username": username, "password": hashed_pw})
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = users_collection.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        token = create_access_token(identity=username)
        return jsonify(access_token=token)

    return jsonify({"error": "Invalid credentials"}), 401

# ------------------ RESUME UPLOAD ------------------

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    text = extract_text(path)
    metadata = extract_metadata(text)

    resumes_collection.insert_one({
        "filename": file.filename,
        "text": text,
        "metadata": metadata,
        "uploaded_at": datetime.utcnow()
    })

    return jsonify({"message": "Resume uploaded successfully"})

# ------------------ RANKING ------------------

@app.route('/rank', methods=['POST'])
@jwt_required()
def rank():
    data = request.json or {}
    job_desc = data.get("job_description", "")
    required_skills = data.get("required_skills", [])

    resumes_data = list(resumes_collection.find())
    resumes = [r["text"] for r in resumes_data]

    results = rank_resumes(resumes, job_desc=job_desc, required_skills=required_skills)
    for i, r in enumerate(results):
        r["metadata"] = resumes_data[i].get("metadata", {})

    analytics = generate_analytics(results, required_skills)

    return jsonify({
        "total_resumes": len(resumes),
        "results": results,
        "analytics": analytics
    })

# ------------------ HOME ------------------

@app.route('/')
def home():
    return "Resume Screening Backend Running"

if __name__ == "__main__":
    app.run(debug=True)
