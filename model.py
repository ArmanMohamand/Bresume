# import re
# from collections import Counter

# COMMON_SKILLS = [
#     "python","java","c++","javascript","react","node","flask","django",
#     "mongodb","sql","docker","aws","git","html","css","typescript",
#     "kubernetes","tensorflow","pandas","numpy"
# ]

# # ---------------- METADATA ----------------
# def extract_metadata(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\+?\d[\d -]{8,}\d', text)

#     return {
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None
#     }


# # ---------------- SKILL EXTRACTION ----------------
# def extract_skills(text):
#     text = text.lower()
#     return [s for s in COMMON_SKILLS if s in text]


# # ---------------- RANKING ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):
#     job_keywords = set(re.findall(r'\w+', job_desc.lower()))
#     results = []

#     for i, resume in enumerate(resumes):
#         skills = extract_skills(resume)

#         if required_skills:
#             req_set = set(s.lower() for s in required_skills)
#             skills = [s for s in skills if s.lower() in req_set]

#         matched_keywords = [k for k in job_keywords if k in resume.lower()]

#         score = len(skills) + len(matched_keywords)

#         results.append({
#             "resume_id": i + 1,
#             "resume_text": resume,
#             "score": score,
#             "matched_skills": skills,
#             "matched_keywords": matched_keywords
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results, required_skills=None):
#     skill_counts = Counter()
#     keyword_counts = Counter()
#     scores = [r["score"] for r in results]

#     for r in results:
#         for s in r["matched_skills"]:
#             skill_counts[s] += 1
#         for k in r.get("matched_keywords", []):
#             keyword_counts[k] += 1

#     return {
#         "skill_distribution": dict(skill_counts),
#         "keyword_distribution": dict(keyword_counts),
#         "average_score": sum(scores) / len(scores) if scores else 0
#     }


# import re
# from collections import Counter

# COMMON_SKILLS = [
#     "python","java","c++","javascript","react","node","flask","django",
#     "mongodb","sql","docker","aws","git","html","css","typescript",
#     "kubernetes","tensorflow","pandas","numpy"
# ]

# # ---------------- METADATA ----------------
# def extract_metadata(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)
#     github = re.search(r'(github\.com\/[A-Za-z0-9_-]+)', text)

#     name_match = re.search(r'Name[:\-]\s*(.*)', text)
#     if not name_match:
#         name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)

#     projects = re.findall(r'Project[:\-]\s*(.*)', text)

#     return {
#         "name": name_match.group(1).strip() if name_match else None,
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None,
#         "github": github.group(0) if github else None,
#         "projects": projects[:3] if projects else []
#     }


# # ---------------- SKILLS ----------------
# def extract_skills(text):
#     text = text.lower()
#     return [s for s in COMMON_SKILLS if s in text]


# # ---------------- RANKING ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):
#     job_keywords = set(re.findall(r'\w+', job_desc.lower()))
#     results = []

#     for i, resume in enumerate(resumes):
#         skills = extract_skills(resume)

#         if required_skills:
#             req_set = set(s.lower() for s in required_skills)
#             skills = [s for s in skills if s in req_set]

#         matched_keywords = [k for k in job_keywords if k in resume.lower()]

#         score = len(skills) + len(matched_keywords)

#         results.append({
#             "resume_id": i + 1,
#             "resume_text": resume,
#             "score": score,
#             "matched_skills": skills,
#             "matched_keywords": matched_keywords
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results):
#     skill_counts = Counter()
#     keyword_counts = Counter()
#     scores = [r["score"] for r in results]

#     for r in results:
#         for s in r["matched_skills"]:
#             skill_counts[s] += 1
#         for k in r.get("matched_keywords", []):
#             keyword_counts[k] += 1

#     return {
#         "skill_distribution": dict(skill_counts),
#         "keyword_distribution": dict(keyword_counts),
#         "average_score": sum(scores) / len(scores) if scores else 0
#     }




import re
from collections import Counter

COMMON_SKILLS = [
    "python","java","c++","javascript","react","node","flask","django",
    "mongodb","sql","docker","aws","git","html","css","typescript",
    "kubernetes","tensorflow","pandas","numpy"
]

# ---------------- METADATA ----------------
# def extract_metadata(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\+?\d[\d -]{8,}\d', text)

#     return {
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None
#     }

def extract_metadata(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'\+?\d[\d -]{8,}\d', text)

    # Capture GitHub links
    github = re.search(r'(https?://github\.com/[^\s]+)', text)

    # Capture LinkedIn (optional, for completeness)
    linkedin = re.search(r'(https?://(www\.)?linkedin\.com/[^\s]+)', text)

    # Capture project names (lines starting with "Project:" or "Projects:")
    projects = re.findall(r'Project[s]?:\s*([^\n,]+)', text, re.IGNORECASE)

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "github": github.group(0) if github else None,
        "linkedin": linkedin.group(0) if linkedin else None,
        "projects": projects if projects else []
    }

# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    text = text.lower()
    return [s for s in COMMON_SKILLS if s in text]

# ---------------- RANKING ----------------
def rank_resumes(resumes, job_desc="", required_skills=None):
    job_keywords = set(re.findall(r'\w+', job_desc.lower()))
    results = []

    for i, resume in enumerate(resumes):
        skills = extract_skills(resume)

        # Only filter if required_skills is non-empty
        if required_skills and len(required_skills) > 0:
            req_set = set(s.lower() for s in required_skills)
            skills = [s for s in skills if s.lower() in req_set]

        matched_keywords = [k for k in job_keywords if k in resume.lower()]
        score = len(skills) + len(matched_keywords)

        results.append({
            "resume_id": i + 1,
            "resume_text": resume,
            "score": score,
            "matched_skills": skills,
            "matched_keywords": matched_keywords
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)

# ---------------- ANALYTICS ----------------
def generate_analytics(results, required_skills=None):
    skill_counts = Counter()
    keyword_counts = Counter()
    scores = [r["score"] for r in results]

    for r in results:
        for s in r["matched_skills"]:
            skill_counts[s] += 1
        for k in r.get("matched_keywords", []):
            keyword_counts[k] += 1

    return {
        "skill_distribution": dict(skill_counts),
        "keyword_distribution": dict(keyword_counts),
        "scores": scores,   # ✅ added so bar chart works
        "average_score": sum(scores) / len(scores) if scores else 0
    }
