# import re

# # ---------------- NORMALIZE TEXT ----------------
# def normalize_text(text):
#     if not text:
#         return ""

#     text = text.lower()

#     replacements = {
#         "node.js": "nodejs",
#         "node js": "nodejs",
#         "express.js": "expressjs",
#         "next.js": "nextjs",
#         "react.js": "react",
#         "mongo db": "mongodb",
#     }

#     for k, v in replacements.items():
#         text = text.replace(k, v)

#     text = re.sub(r"[^a-z0-9+# ]", " ", text)
#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# # ---------------- CONTACT ----------------
# def extract_contact(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\b\d{10}\b', text)

#     return {
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None
#     }


# # ---------------- LINKS (FIXED) ----------------
# def extract_links(text):
#     github = re.search(r'(https?://)?(www\.)?github\.com/[^\s]+', text)
#     linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/[^\s]+', text)

#     return {
#         "github": github.group(0) if github else None,
#         "linkedin": linkedin.group(0) if linkedin else None
#     }


# # ---------------- NAME EXTRACTION ----------------
# def extract_name(text):
#     lines = text.split("\n")

#     for line in lines[:15]:
#         line = line.strip()

#         if (
#             2 <= len(line.split()) <= 4 and
#             not re.search(r'@|http|\d|btech|education|college|university', line.lower())
#         ):
#             return line

#     return None


# # ---------------- SKILLS (FINAL CLEAN) ----------------
# def extract_skills(text):
#     text = normalize_text(text)

#     skill_keywords = [
#         # Languages
#         "python", "java", "c++", "c", "javascript", "typescript",

#         # Frontend
#         "react", "nextjs", "vue", "angular", "tailwind", "bootstrap", "html", "css",

#         # Backend
#         "nodejs", "expressjs", "flask", "django",

#         # Database
#         "mongodb", "sql", "mysql", "postgresql",

#         # Tools
#         "docker", "aws", "git",

#         # Concepts
#         "dsa", "api", "rest"
#     ]

#     found = set()

#     for skill in skill_keywords:
#         if skill == "c":
#             if re.search(r"\bc\b", text):
#                 found.add(skill)
#         else:
#             if re.search(rf"\b{skill}\b", text):
#                 found.add(skill)

#     # smart detection
#     if "data structure" in text or "algorithm" in text:
#         found.add("dsa")

#     return list(found)


# # ---------------- METADATA ----------------
# def extract_metadata(text):
#     contact = extract_contact(text)
#     links = extract_links(text)

#     return {
#         "name": extract_name(text),
#         "email": contact["email"],
#         "phone": contact["phone"],
#         "github": links["github"],
#         "linkedin": links["linkedin"],
#     }
# def extract_projects(text):
#     projects = []
#     links = []

#     # find project-like lines
#     lines = text.split("\n")

#     for line in lines:
#         if any(word in line.lower() for word in ["project", "app", "system", "website"]):
#             if len(line) < 120:
#                 projects.append(line.strip())

#         # extract links
#         link = re.search(r'https?://[^\s]+', line)
#         if link:
#             links.append(link.group(0))

#     return {
#         "projects": list(set(projects))[:5],   # limit to 5
#         "project_links": list(set(links))[:5]
#     }
# def extract_links(text):
#     text = text.lower()

#     github = re.search(r'(https?://)?(www\.)?github\.com/[a-zA-Z0-9_-]+', text)
#     linkedin = re.search(r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+', text)

#     return {
#         "github": github.group(0) if github else None,
#         "linkedin": linkedin.group(0) if linkedin else None
#     }

# def extract_name(text):
#     lines = text.strip().split("\n")

#     for line in lines[:5]:  # check top 5 lines only
#         line = line.strip()

#         if len(line.split()) <= 4 and not any(char.isdigit() for char in line):
#             return line

#     return None
# # ---------------- RANKING ----------------

# # def rank_resumes(resumes, job_desc="", required_skills=None):

# #     results = []

# #     for i, resume in enumerate(resumes):

# #         raw_text = resume.get("text", "")

# #         skills_found = extract_skills(raw_text)
# #         metadata = extract_metadata(raw_text)

# #         # ✅ SCORE = NUMBER OF SKILLS
# #         final_score = len(skills_found)

# #         # DEBUG
# #         print("\n--- DEBUG ---")
# #         print("NAME:", metadata["name"])
# #         print("SKILLS:", skills_found)
# #         print("SCORE:", final_score)

# #         results.append({
# #             "resume_id": i + 1,
# #             "score": final_score,

# #             "skills": skills_found,

# #             "email": metadata["email"],
# #             "phone": metadata["phone"],

# #             "metadata": metadata
# #         })

# #     return sorted(results, key=lambda x: x["score"], reverse=True)



# import re
# # from sklearn.feature_extraction.text import TfidfVectorizer
# # from sklearn.metrics.pairwise import cosine_similarity


# # ---------------- CONTACT ----------------
# def extract_contact(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)

#     return {
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None
#     }


# # ---------------- NAME ----------------
# def extract_name(text):
#     lines = text.split("\n")

#     for line in lines[:20]:   
#         line = line.strip()

#         if (
#             2 <= len(line.split()) <= 4 and
#             not re.search(r'@|http|\d|btech|education|college|university|project', line.lower())
#         ):
#             return line

#     return None

# # ---------------- SKILLS ----------------
# SKILLS_DB = [
#     "python", "java", "c++", "c", "javascript",
#     "react", "next.js", "node.js", "express.js",
#     "flask", "django", "mongodb", "sql",
#     "docker", "aws", "html", "css", "tailwind"
# ]

# def extract_skills(text):
#     text = text.lower()

#     normalized = text.replace("node.js", "nodejs") \
#                      .replace("next.js", "nextjs") \
#                      .replace("express.js", "expressjs")

#     skills = []
#     for s in SKILLS_DB:
#         if s.replace(".", "") in normalized:
#             skills.append(s)

#     return skills


# # ---------------- LINKS ----------------
# def extract_links(text):
#     text = text.replace("\n", " ")

#     github = None
#     linkedin = None

#     # direct URLs
#     github_url = re.search(r'https?://github\.com/[^\s]+', text, re.IGNORECASE)
#     linkedin_url = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text, re.IGNORECASE)

#     if github_url:
#         github = github_url.group(0)

#     if linkedin_url:
#         linkedin = linkedin_url.group(0)

#     # username-based fallback
#     if not github:
#         g_match = re.search(r'github\s*[:\-]?\s*([A-Za-z0-9_-]{3,})', text, re.IGNORECASE)
#         if g_match:
#             github = f"https://github.com/{g_match.group(1)}"

#     if not linkedin:
#         l_match = re.search(r'linkedin\s*[:\-]?\s*([A-Za-z ]{3,})', text, re.IGNORECASE)
#         if l_match:
#             name = l_match.group(1)
#             name = re.split(r'github|email|phone', name, flags=re.IGNORECASE)[0]
#             name = " ".join(name.strip().split())
#             linkedin = f"https://linkedin.com/in/{name.replace(' ', '-')}"

#     return {
#         "github": github,
#         "linkedin": linkedin
#     }


# # ---------------- PROJECTS ----------------
# def extract_projects(text):
#     projects = []
#     links = []

#     lines = text.split("\n")

#     for line in lines:
#         l = line.lower()

#         # better detection
#         if any(word in l for word in ["project", "developed", "built", "application", "system"]):
#             if 20 < len(line) < 120:
#                 projects.append(line.strip())

#         # extract links
#         found_links = re.findall(r'https?://[^\s]+', line)
#         for link in found_links:
#             links.append(link)

#     return {
#         "projects": list(set(projects))[:5],
#         "project_links": list(set(links))[:5]
#     }
# def rank_resumes(resumes, job_desc="", required_skills=None):

#     results = []

#     for i, resume in enumerate(resumes):

#         raw_text = resume.get("text", "")

#         skills_found = extract_skills(raw_text)
#         metadata = extract_metadata(raw_text)

#         # ✅ SCORE = NUMBER OF SKILLS
#         final_score = len(skills_found)

#         # DEBUG
#         print("\n--- DEBUG ---")
#         print("NAME:", metadata["name"])
#         print("SKILLS:", skills_found)
#         print("SCORE:", final_score)

#         results.append({
#             "resume_id": i + 1,
#             "score": final_score,

#             "skills": skills_found,

#             "email": metadata["email"],
#             "phone": metadata["phone"],

#             "metadata": metadata
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)



# # # ---------------- RANKING ----------------
# # def rank_resumes(resumes, job_desc="", required_skills=None):

# #     texts = [job_desc] + [r.get("text", "") for r in resumes]

# #     vectorizer = TfidfVectorizer(stop_words="english")
# #     tfidf = vectorizer.fit_transform(texts)

# #     job_vector = tfidf[0]
# #     resume_vectors = tfidf[1:]

# #     similarities = cosine_similarity(job_vector, resume_vectors)[0]

# #     results = []

# #     for i, resume in enumerate(resumes):
# #         text = resume.get("text", "")

# #         name = extract_name(text)
# #         contact = extract_contact(text)
# #         skills = extract_skills(text)
# #         links = extract_links(text)
# #         projects = extract_projects(text)

# #         score = float(similarities[i])

# #         results.append({
# #             "resume_id": i + 1,
# #             "filename": resume.get("filename"),
# #             "uploaded_by": resume.get("uploaded_by"),

# #             "score": score,
# #             "name": name,
# #             "skills": skills,

# #             "email": contact["email"],
# #             "phone": contact["phone"],
# #             "github": links["github"],
# #             "linkedin": links["linkedin"],

# #             "projects": projects
# #         })

# #     return sorted(results, key=lambda x: x["score"], reverse=True)


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results):
#     scores = [r["score"] for r in results]

#     return {
#         "scores": scores,
#         "average_score": sum(scores) / len(scores) if scores else 0
#     }

import re

# ---------------- CONTACT ----------------
def extract_contact(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None
    }


# ---------------- NAME ----------------
def extract_name(text):
    lines = text.split("\n")

    skip_words = [
        "resume", "skills", "education", "projects",
        "experience", "certifications", "technical", "summary"
    ]

    for line in lines[:15]:
        line = line.strip()

        if not line:
            continue

        if any(word in line.lower() for word in skip_words):
            continue

        if 2 <= len(line.split()) <= 4 and line.replace(" ", "").isalpha():
            return line

    return None


# ---------------- SKILLS ----------------
SKILLS_DB = [
    "python", "java", "c++", "c", "javascript",
    "react", "next.js", "node.js", "express.js",
    "flask", "django", "mongodb", "sql",
    "docker", "aws", "html", "css", "tailwind"
]

def extract_skills(text):
    text = text.lower()

    normalized = (
        text.replace("node.js", "nodejs")
            .replace("next.js", "nextjs")
            .replace("express.js", "expressjs")
    )

    return [s for s in SKILLS_DB if s.replace(".", "") in normalized]


# ---------------- LINKS ----------------
def extract_links(text):
    text = text.replace("\n", " ")

    github = None
    linkedin = None

    github_url = re.search(r'https?://github\.com/[^\s]+', text, re.IGNORECASE)
    linkedin_url = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text, re.IGNORECASE)

    if github_url:
        github = github_url.group(0)

    if linkedin_url:
        linkedin = linkedin_url.group(0)

    return {
        "github": github,
        "linkedin": linkedin
    }


# ---------------- PROJECTS ----------------
def extract_projects(text):
    projects = []
    links = []

    lines = text.split("\n")

    for line in lines:
        l = line.lower()

        # detect project-like lines
        if any(word in l for word in ["project", "built", "developed", "system", "application"]):
            clean = line.strip()
            if 20 < len(clean) < 200:
                projects.append(clean)

        # extract links
        found_links = re.findall(r'https?://[^\s]+', line)
        links.extend(found_links)

    return {
        "projects": list(set(projects))[:5],
        "project_links": list(set(links))[:5]
    }


# ---------------- RANKING (FINAL RULE-BASED) ----------------
def rank_resumes(resumes, job_desc="", required_skills=None):

    results = []

    req_skills = set([s.lower() for s in required_skills]) if required_skills else set()

    for i, resume in enumerate(resumes):

        text = resume.get("text", "")

        skills = extract_skills(text)
        contact = extract_contact(text)
        links = extract_links(text)
        projects = extract_projects(text)
        name = extract_name(text)

        # ---------------- SCORING ----------------
        score = 0

        # 1. skill count
        score += len(skills)

        # 2. required skills match (higher weight)
        if req_skills:
            matched = [s for s in skills if s in req_skills]
            score += len(matched) * 2

        # 3. project bonus
        score += len(projects["projects"])

        # 4. GitHub / LinkedIn bonus
        if links["github"]:
            score += 1
        if links["linkedin"]:
            score += 1

        results.append({
            "resume_id": i + 1,
            "name": name,
            "score": score,

            "skills": skills,

            "email": contact["email"],
            "phone": contact["phone"],

            "github": links["github"],
            "linkedin": links["linkedin"],

            "projects": projects["projects"],
            "project_links": projects["project_links"]
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)


# ---------------- ANALYTICS ----------------
def generate_analytics(results):
    scores = [r["score"] for r in results]

    return {
        "scores": scores,
        "average_score": sum(scores) / len(scores) if scores else 0
    }