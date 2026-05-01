from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

from db import users_collection, resumes_collection
from model import rank_resumes, generate_analytics, extract_metadata

app = Flask(__name__)

# ---------------- JWT CONFIG ----------------
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

if not app.config["JWT_SECRET_KEY"]:
    raise Exception("JWT_SECRET_KEY is missing")

jwt = JWTManager(app)

# ---------------- CORS ----------------
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:5173",
        "https://fresume-nine.vercel.app",
        "https://fresume-git-main-arman-mohamand-projects.vercel.app"
    ]
}})


# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)

    users_collection.insert_one({
        "username": username,
        "password": hashed_pw
    })

    return jsonify({"message": "User registered successfully"}), 201


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = users_collection.find_one({"username": data.get("username")})

    if not user or not check_password_hash(user["password"], data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["username"])

    return jsonify({"access_token": token}), 200


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
@jwt_required()
def upload_resume():
    data = request.get_json()

    filename = data.get("filename")
    text = data.get("text")

    if not filename or not text:
        return jsonify({"error": "Missing filename or text"}), 400

    if len(text) > 200000:
        return jsonify({"error": "Resume too large"}), 400

    user = get_jwt_identity()

    metadata = extract_metadata(text)

    resumes_collection.insert_one({
        "filename": filename,
        "text": text,
        "metadata": metadata,
        "uploaded_by": user,
        "uploaded_at": datetime.utcnow()
    })

    return jsonify({"message": "Resume uploaded successfully"}), 201


# ---------------- RANK ----------------
@app.route("/rank", methods=["POST"])
@jwt_required()
def rank():
    data = request.get_json()

    skills = data.get("required_skills", [])
    job_desc = data.get("job_description", "")

    resumes_data = list(resumes_collection.find({}, {"_id": 0}))
    resumes = [r["text"] for r in resumes_data]

    results = rank_resumes(resumes, job_desc, skills)

    for r in results:
        idx = r["resume_id"] - 1
        r["metadata"] = resumes_data[idx].get("metadata", {}) if 0 <= idx < len(resumes_data) else {}

    analytics = generate_analytics(results, skills)

    return jsonify({
        "total_resumes": len(resumes),
        "results": results,
        "analytics": analytics
    })


# ---------------- HEALTH ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend running successfully"})


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import (
#     JWTManager, create_access_token,
#     jwt_required, get_jwt_identity
# )
# from werkzeug.security import generate_password_hash, check_password_hash
# from datetime import datetime
# import os

# from db import users_collection, resumes_collection
# from model import rank_resumes, generate_analytics, extract_metadata

# app = Flask(__name__)

# # ---------------- JWT CONFIG ----------------
# app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret")
# jwt = JWTManager(app)

# # ---------------- CORS ----------------
# CORS(app, resources={r"/*": {"origins": "*"}})


# # ---------------- REGISTER ----------------
# @app.route("/register", methods=["POST"])
# def register():
#     data = request.get_json()

#     if users_collection.find_one({"username": data["username"]}):
#         return jsonify({"error": "User already exists"}), 400

#     users_collection.insert_one({
#         "username": data["username"],
#         "password": generate_password_hash(data["password"])
#     })

#     return jsonify({"message": "registered"})


# # ---------------- LOGIN ----------------
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()

#     user = users_collection.find_one({"username": data["username"]})

#     if not user or not check_password_hash(user["password"], data["password"]):
#         return jsonify({"error": "invalid credentials"}), 401

#     token = create_access_token(identity=user["username"])
#     return jsonify({"access_token": token})


# # ---------------- UPLOAD + AUTO RANK ----------------
# @app.route("/upload", methods=["POST"])
# @jwt_required()
# def upload():
#     user = get_jwt_identity()
#     data = request.get_json()

#     text = data.get("text", "")
#     filename = data.get("filename", "")

#     if not text or not filename:
#         return jsonify({"error": "Missing data"}), 400

#     # Extract metadata
#     metadata = extract_metadata(text)

#     # Save resume
#     resumes_collection.insert_one({
#         "username": user,
#         "filename": filename,
#         "text": text,
#         "metadata": metadata,
#         "score": 0
#     })

#     # Fetch all resumes for user
#     resumes = list(resumes_collection.find({"username": user}))
#     texts = [r["text"] for r in resumes]

#     # Run ranking
#     results = rank_resumes(texts, "", [])

#     # Save scores back to DB
#     for r in results:
#         idx = r["resume_id"] - 1

#         if 0 <= idx < len(resumes):
#             resumes_collection.update_one(
#                 {"_id": resumes[idx]["_id"]},
#                 {"$set": {"score": r["score"]}}
#             )

#     # Generate analytics
#     analytics = generate_analytics(results)

#     return jsonify({
#         "message": "Uploaded + Auto Ranked",
#         "analytics": analytics
#     })


# # ---------------- CANDIDATES ----------------
# @app.route("/candidates", methods=["GET"])
# @jwt_required()
# def candidates():
#     user = get_jwt_identity()

#     resumes = list(resumes_collection.find({"username": user}))

#     result = []

#     for r in resumes:
#         meta = r.get("metadata", {})

#         result.append({
#             "name": meta.get("name"),
#             "email": meta.get("email"),
#             "phone": meta.get("phone"),
#             "github": meta.get("github"),
#             "score": r.get("score", 0),
#             "filename": r.get("filename")
#         })

#     return jsonify(result)


# # ---------------- HEALTH ----------------
# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({"message": "Backend running"})


# # ---------------- RUN ----------------
# if __name__ == "__main__":
#     app.run(debug=True)