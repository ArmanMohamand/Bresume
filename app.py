from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from dotenv import load_dotenv
from bson import ObjectId
from datetime import datetime

import os
import fitz

from db import (
    users_collection,
    resumes_collection,
    jobdesc_collection
)

from model import (
    rank_resumes,
    generate_analytics
)

# ---------------- INIT ----------------
load_dotenv()

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY"
)

jwt = JWTManager(app)

CORS(app)

# ---------------- ADMIN ----------------
ADMIN_EMAILS = [
    "khanarman23218@gmail.com",
    "236301052@gkv.ac.in",
]

# ---------------- HOME ----------------
@app.route("/")
def home():

    return jsonify({
        "message": "Backend running"
    })


# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if users_collection.find_one({
        "email": data["email"]
    }):

        return jsonify({
            "error": "Email exists"
        }), 400

    users_collection.insert_one({

        "email": data["email"],

        "username": data["username"],

        "password": generate_password_hash(
            data["password"]
        )
    })

    return jsonify({
        "message": "Registered"
    }), 201


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    user = users_collection.find_one({
        "email": data["email"]
    })

    if not user:

        return jsonify({
            "error": "User not found"
        }), 404

    if not check_password_hash(
        user["password"],
        data["password"]
    ):

        return jsonify({
            "error": "Invalid credentials"
        }), 401

    role = (
        "admin"
        if user["email"] in ADMIN_EMAILS
        else "employee"
    )

    token = create_access_token(

        identity=user["email"],

        additional_claims={

            "username": user["username"],

            "role": role
        }
    )

    return jsonify({
        "access_token": token
    })

# ---------------- UPLOAD RESUME ----------------
@app.route("/upload", methods=["POST"])
@jwt_required()
def upload():

    data = request.get_json(silent=True)

    text = None
    filename = None

    linkedin = None
    github = None
    project_links = []

    if data and data.get("text"):

        text = data["text"]

        filename = data.get("filename")

        linkedin = data.get("linkedin")

        github = data.get("github")

        project_links = data.get(
            "project_links",
            []
        )

    else:

        file = request.files.get("file")

        if file:

            filename = file.filename

            if filename.endswith(".pdf"):

                doc = fitz.open(
                    stream=file.read(),
                    filetype="pdf"
                )

                text = " ".join([
                    page.get_text()
                    for page in doc
                ])

            else:

                text = file.read().decode(
                    "utf-8",
                    errors="ignore"
                )

    if not text or text.strip() == "":

        return jsonify({
            "error": "Could not extract text from resume"
        }), 400

    current_email = get_jwt_identity()

    user = users_collection.find_one({
        "email": current_email
    })

    resumes_collection.insert_one({

        "filename": filename,

        "text": text,

        "uploaded_by": current_email,

        "username": user.get(
            "username",
            "Unknown"
        ),

        # NEW
        "linkedin": linkedin,

        "github": github,

        "project_links": project_links
    })

    return jsonify({
        "message": "Uploaded"
    })


# ---------------- RANK ----------------
@app.route("/rank", methods=["POST"])
@jwt_required()
def rank():

    data = request.get_json()

    job_description = data.get(
        "job_description",
        ""
    )

    required_skills = data.get(
        "required_skills",
        []
    )

    current_user_email = get_jwt_identity()

    resumes_db = list(
        resumes_collection.find()
    )

    if not resumes_db:

        return jsonify({
            "error": "No resumes found"
        }), 400

    resumes = []

    for r in resumes_db:

      resumes.append({

    "id": str(r["_id"]),

    "filename": r.get(
        "filename",
        "Resume.pdf"
    ),

    "text": r.get("text", ""),

    "username": r.get(
        "username",
        "Unknown"
    ),
     # NEW
    "linkedin": r.get("linkedin"),

    "github": r.get("github"),

    "project_links": r.get(
        "project_links",
        []
    )
    
})

    ranked = rank_resumes(

        resumes,

        job_description,

        required_skills,

        current_user_email
    )

    analytics = generate_analytics(
        ranked
    )

    return jsonify({

        "ranked": ranked,

        "analytics": analytics
    })


# ---------------- SAVE JOB ----------------
@app.route("/jobdesc/save", methods=["POST"])
@jwt_required()
def save_job():

    if get_jwt().get("role") != "admin":

        return jsonify({
            "error": "Only admin allowed"
        }), 403

    data = request.get_json()

    job = {

        "desc": data.get("desc"),

        "skills": data.get("skills", []),

        "endTime": data.get("endTime")
    }

    result = jobdesc_collection.insert_one(
        job
    )

    job["_id"] = str(
        result.inserted_id
    )

    return jsonify({
        "job": job
    })


# ---------------- LIST JOBS ----------------
@app.route("/jobdesc/list", methods=["GET"])
@jwt_required()
def list_jobs():

    jobs = list(
        jobdesc_collection.find()
    )

    now = datetime.utcnow()

    for j in jobs:

        j["_id"] = str(j["_id"])

        try:

            if j.get("endTime"):

                end_time = datetime.fromisoformat(
                    j["endTime"]
                )

                j["expired"] = end_time < now

            else:

                j["expired"] = False

        except:

            j["expired"] = False

    return jsonify(jobs), 200


# ---------------- UPDATE JOB ----------------
@app.route(
    "/jobdesc/update/<id>",
    methods=["PUT"]
)
@jwt_required()
def update_job(id):

    if get_jwt().get("role") != "admin":

        return jsonify({
            "error": "Only admin allowed"
        }), 403

    if not ObjectId.is_valid(id):

        return jsonify({
            "error": "Invalid ID"
        }), 400

    data = request.get_json()

    update_data = {

        "desc": data.get("desc"),

        "skills": data.get("skills", []),

        "endTime": data.get("endTime")
    }

    jobdesc_collection.update_one(

        {"_id": ObjectId(id)},

        {"$set": update_data}
    )

    update_data["_id"] = id

    return jsonify({
        "job": update_data
    })


# ---------------- DELETE RESUME ----------------
@app.route(
    "/delete_resume/<resume_id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_resume(resume_id):

    if not ObjectId.is_valid(resume_id):

        return jsonify({
            "error": "Invalid resume ID"
        }), 400

    current_user_email = get_jwt_identity()

    resume = resumes_collection.find_one({
        "_id": ObjectId(resume_id)
    })

    if not resume:

        return jsonify({
            "error": "Resume not found"
        }), 404

    is_admin = (
        current_user_email in ADMIN_EMAILS
    )

    if (
        resume.get("uploaded_by")
        != current_user_email
        and not is_admin
    ):

        return jsonify({
            "error": "Unauthorized"
        }), 403

    resumes_collection.delete_one({
        "_id": ObjectId(resume_id)
    })

    return jsonify({
        "message": "Resume deleted successfully"
    }), 200


# ---------------- DELETE JOB ----------------
@app.route(
    "/jobdesc/delete/<id>",
    methods=["DELETE"]
)
@jwt_required()
def delete_job(id):

    if get_jwt().get("role") != "admin":

        return jsonify({
            "error": "Only admin allowed"
        }), 403

    if not ObjectId.is_valid(id):

        return jsonify({
            "error": "Invalid ID"
        }), 400

    result = jobdesc_collection.delete_one({
        "_id": ObjectId(id)
    })

    if result.deleted_count == 0:

        return jsonify({
            "error": "Job not found"
        }), 404

    return jsonify({
        "message": "Deleted successfully"
    }), 200


# ---------------- RUN ----------------
if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 10000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )