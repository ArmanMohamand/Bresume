# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_jwt_extended import (
#     JWTManager,
#     create_access_token,
#     jwt_required,
#     get_jwt_identity,
#     get_jwt
# )
# from werkzeug.security import generate_password_hash, check_password_hash
# from dotenv import load_dotenv

# import os
# import sys

# from db import users_collection, resumes_collection
# from model import rank_resumes, generate_analytics

# # ---------------- LOAD ENV ----------------
# load_dotenv()

# app = Flask(__name__)

# # ---------------- JWT CONFIG ----------------
# app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
# app.config["JWT_HEADER_TYPE"] = "Bearer"
# app.config["JWT_TOKEN_LOCATION"] = ["headers"]

# if not app.config["JWT_SECRET_KEY"]:
#     raise Exception("JWT_SECRET_KEY is missing")

# jwt = JWTManager(app)

# # ---------------- CORS ----------------
# CORS(
#     app,
#     resources={
#         r"/*": {
#             "origins": [
#                 "http://localhost:5173",
#                 "https://fresume-nine.vercel.app",
#                 "https://fresume-git-main-arman-mohamand-projects.vercel.app",
#             ],
#             "methods": ["GET", "POST", "DELETE", "OPTIONS"],
#             "allow_headers": ["Authorization", "Content-Type"],
#         }
#     },
# )

# # ---------------- ADMIN EMAILS ----------------
# ADMIN_EMAILS = [
#     "khanarman23218@gmail.com",
#     "236301052@gkv.ac.in",
# ]

# # ---------------- HOME ----------------
# @app.route("/", methods=["GET"])
# def home():
#     return jsonify({"message": "Backend running successfully"})


# # ---------------- REGISTER ----------------
# @app.route("/register", methods=["POST"])
# def register():
#     data = request.get_json()

#     if not data:
#         return jsonify({"error": "Missing request body"}), 400

#     email = data.get("email")
#     username = data.get("username")
#     password = data.get("password")

#     if not email or not username or not password:
#         return jsonify({"error": "Missing fields"}), 400

#     if users_collection.find_one({"email": email}):
#         return jsonify({"error": "Email already registered"}), 400

#     if users_collection.find_one({"username": username}):
#         return jsonify({"error": "Username already taken"}), 400

#     hashed_pw = generate_password_hash(password)

#     users_collection.insert_one({
#         "email": email,
#         "username": username,
#         "password": hashed_pw,
#     })

#     return jsonify({"message": "User registered successfully"}), 201


# # ---------------- LOGIN ----------------
# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()

#     if not data:
#         return jsonify({"error": "Missing request body"}), 400

#     user = users_collection.find_one({
#         "email": data.get("email")
#     })

#     if not user:
#         return jsonify({"error": "User not found"}), 404

#     if not check_password_hash(user["password"], data.get("password")):
#         return jsonify({"error": "Invalid credentials"}), 401

#     role = "admin" if user["email"] in ADMIN_EMAILS else "employee"

#     # ✅ FIXED JWT TOKEN
#     token = create_access_token(
#         identity=user["email"],
#         additional_claims={
#             "username": user["username"],
#             "role": role,
#         }
#     )

#     return jsonify({"access_token": token}), 200


# # ---------------- UPLOAD ----------------
# @app.route("/upload", methods=["POST"])
# @jwt_required()
# def upload_resume():
#     try:
#         # ✅ current_user is now email string
#         current_user = get_jwt_identity()

#         data = request.get_json(force=True, silent=True)

#         if not data:
#             return jsonify({
#                 "error": "No JSON data received"
#             }), 422

#         filename = data.get("filename", "")
#         text = data.get("text", "")

#         if not filename:
#             return jsonify({
#                 "error": "Filename missing"
#             }), 422

#         if not text:
#             return jsonify({
#                 "error": "Text missing"
#             }), 422

#         if not text.strip():
#             return jsonify({
#                 "error": "Text empty"
#             }), 422

#         resumes_collection.insert_one({
#             "filename": filename,
#             "text": text,
#             "uploaded_by": current_user
#         })

#         return jsonify({
#             "message": "Resume uploaded successfully"
#         }), 201

#     except Exception as e:
#         print("UPLOAD ERROR:", str(e), file=sys.stderr)

#         return jsonify({
#             "error": str(e)
#         }), 500


# # ---------------- RANK ----------------
# @app.route("/rank", methods=["POST"])
# @jwt_required()
# def rank():
#     try:
#         current_user = get_jwt_identity()

#         if not current_user:
#             return jsonify({"error": "Unauthorized"}), 401

#         data = request.get_json(force=True, silent=True)

#         if not data:
#             return jsonify({"error": "Missing request body"}), 422

#         job_description = data.get("job_description", "")
#         required_skills = data.get("required_skills", [])

#         resumes = list(
#             resumes_collection.find({}, {"_id": 0})
#         )

#         ranked = rank_resumes(
#             resumes,
#             job_description,
#             required_skills
#         )

#         analytics = generate_analytics(ranked)

#         return jsonify({
#             "ranked": ranked,
#             "analytics": analytics
#         }), 200

#     except Exception as e:
#         print("RANK ERROR:", str(e), file=sys.stderr)

#         return jsonify({
#             "error": str(e)
#         }), 500


# # ---------------- JOBDESC SAVE ----------------
# @app.route("/jobdesc/save", methods=["POST"])
# @jwt_required()
# def save_jobdesc():
#     claims = get_jwt()

#     if claims.get("role") != "admin":
#         return jsonify({
#             "error": "Only admins can add job descriptions"
#         }), 403

#     return jsonify({
#         "message": "Job description saved"
#     }), 201


# # ---------------- JOBDESC DELETE ----------------
# @app.route("/jobdesc/delete/<id>", methods=["DELETE"])
# @jwt_required()
# def delete_jobdesc(id):
#     claims = get_jwt()

#     if claims.get("role") != "admin":
#         return jsonify({
#             "error": "Only admins can delete job descriptions"
#         }), 403

#     return jsonify({
#         "message": "Job description deleted"
#     }), 200


# # ---------------- JOBDESC LIST ----------------
# @app.route("/jobdesc/list", methods=["GET"])
# @jwt_required()
# def list_jobdesc():
#     entries = list(
#         resumes_collection.find({}, {"_id": 0})
#     )

#     return jsonify(entries), 200


# # ---------------- RUN ----------------
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 5000))

#     app.run(
#         host="0.0.0.0",
#         port=port,
#         debug=True
#     )


from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from bson import ObjectId

import os
import sys

from db import users_collection, resumes_collection
from model import rank_resumes, generate_analytics

# ✅ NEW COLLECTION
from db import db
jobdesc_collection = db["job_descriptions"]

# ---------------- LOAD ENV ----------------
load_dotenv()

app = Flask(__name__)

# ---------------- JWT CONFIG ----------------
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_HEADER_TYPE"] = "Bearer"
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

if not app.config["JWT_SECRET_KEY"]:
    raise Exception("JWT_SECRET_KEY is missing")

jwt = JWTManager(app)

# ---------------- CORS ----------------
CORS(
    app,
    resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://fresume-nine.vercel.app",
                "https://fresume-git-main-arman-mohamand-projects.vercel.app",
            ],
            "methods": ["GET", "POST", "DELETE", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"],
        }
    },
)

# ---------------- ADMIN EMAILS ----------------
ADMIN_EMAILS = [
    "khanarman23218@gmail.com",
    "236301052@gkv.ac.in",
]

# ---------------- HOME ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend running successfully"})


# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already registered"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already taken"}), 400

    hashed_pw = generate_password_hash(password)

    users_collection.insert_one({
        "email": email,
        "username": username,
        "password": hashed_pw,
    })

    return jsonify({"message": "User registered successfully"}), 201


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing request body"}), 400

    user = users_collection.find_one({
        "email": data.get("email")
    })

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user["password"], data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    role = "admin" if user["email"] in ADMIN_EMAILS else "employee"

    token = create_access_token(
        identity=user["email"],
        additional_claims={
            "username": user["username"],
            "role": role,
        }
    )

    return jsonify({"access_token": token}), 200


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["POST"])
@jwt_required()
def upload_resume():
    try:
        current_user = get_jwt_identity()

        data = request.get_json(force=True, silent=True)

        if not data:
            return jsonify({"error": "No JSON data"}), 422

        filename = data.get("filename", "")
        text = data.get("text", "")

        if not filename or not text.strip():
            return jsonify({"error": "Invalid data"}), 422

        resumes_collection.insert_one({
            "filename": filename,
            "text": text,
            "uploaded_by": current_user
        })

        return jsonify({"message": "Resume uploaded successfully"}), 201

    except Exception as e:
        print("UPLOAD ERROR:", str(e), file=sys.stderr)
        return jsonify({"error": str(e)}), 500


# ---------------- RANK ----------------
@app.route("/rank", methods=["POST"])
@jwt_required()
def rank():
    try:
        data = request.get_json()

        job_description = data.get("job_description", "")
        required_skills = data.get("required_skills", [])

        resumes = list(resumes_collection.find({}, {"_id": 0}))

        ranked = rank_resumes(resumes, job_description, required_skills)
        analytics = generate_analytics(ranked)

        return jsonify({
            "ranked": ranked,
            "analytics": analytics
        }), 200

    except Exception as e:
        print("RANK ERROR:", str(e), file=sys.stderr)
        return jsonify({"error": str(e)}), 500


# ================= JOB DESCRIPTION =================

# ---------------- SAVE ----------------
@app.route("/jobdesc/save", methods=["POST"])
@jwt_required()
def save_jobdesc():
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "error": "Only admins can add job descriptions"
        }), 403

    data = request.get_json()

    job = {
        "desc": data.get("desc"),
        "skills": data.get("skills"),
        "endTime": data.get("endTime")
    }

    result = jobdesc_collection.insert_one(job)

    job["_id"] = str(result.inserted_id)

    return jsonify({
        "message": "Job description saved",
        "job": job
    }), 201


# ---------------- LIST ----------------
@app.route("/jobdesc/list", methods=["GET"])
@jwt_required()
def list_jobdesc():
    jobs = list(jobdesc_collection.find())

    for job in jobs:
        job["_id"] = str(job["_id"])

    return jsonify(jobs), 200


# ---------------- DELETE ----------------
@app.route("/jobdesc/delete/<id>", methods=["DELETE"])
@jwt_required()
def delete_jobdesc(id):
    claims = get_jwt()

    if claims.get("role") != "admin":
        return jsonify({
            "error": "Only admins can delete job descriptions"
        }), 403

    jobdesc_collection.delete_one({"_id": ObjectId(id)})

    return jsonify({
        "message": "Deleted successfully"
    }), 200


# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )