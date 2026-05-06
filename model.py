# import re
# from collections import Counter

# COMMON_SKILLS = [
#     "python",
#     "java",
#     "c++",
#     "javascript",
#     "react",
#     "node",
#     "flask",
#     "django",
#     "mongodb",
#     "sql",
#     "docker",
#     "aws",
#     "git",
#     "html",
#     "css",
#     "typescript",
#     "kubernetes",
#     "tensorflow",
#     "pandas",
#     "numpy",
# ]

# # ---------------- METADATA ----------------
# def extract_metadata(text):
#     # Email + phone
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)

#     # GitHub
#     github = re.search(
#         r'(https?://github\.com/[^\s]+|GitHub:\s*[A-Za-z0-9_-]+)',
#         text,
#         re.IGNORECASE
#     )

#     # LinkedIn
#     linkedin = re.search(
#         r'(https?://(www\.)?linkedin\.com/[^\s]+|LinkedIn:\s*[A-Za-z0-9_-]+)',
#         text,
#         re.IGNORECASE
#     )

#     # Name
#     name_match = re.search(r'Name[:\-]\s*(.*)', text)

#     if not name_match:
#         name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)

#     # Projects
#     projects_section = re.findall(
#         r'Projects?\s*[\n\r]+([\s\S]+?)(?=\n\n|$)',
#         text,
#         re.IGNORECASE
#     )

#     projects = []
#     project_links = []

#     if projects_section:
#         for line in projects_section[0].splitlines():
#             line = line.strip()

#             if line and not line.lower().startswith("projects"):
#                 projects.append(line)

#                 url_match = re.search(r'https?://[^\s\)]+', line)

#                 if url_match:
#                     project_links.append(url_match.group(0))

#     return {
#         "name": name_match.group(1).strip() if name_match else None,
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None,
#         "github": github.group(0) if github else None,
#         "linkedin": linkedin.group(0) if linkedin else None,
#         "projects": projects,
#         "project_links": project_links,
#     }


# # ---------------- SKILL EXTRACTION ----------------
# def extract_skills(text):
#     if not text:
#         return []

#     text = text.lower()

#     return [s for s in COMMON_SKILLS if s in text]


# # ---------------- RANKING ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):
#     job_keywords = set(
#         re.findall(r'\w+', job_desc.lower())
#     )

#     results = []

#     for i, resume in enumerate(resumes):

#         resume_text = resume.get("text", "")

#         if not isinstance(resume_text, str):
#             resume_text = str(resume_text)

#         # Extract skills
#         skills = extract_skills(resume_text)

#         # Filter required skills
#         if required_skills and len(required_skills) > 0:
#             req_set = set(
#                 s.lower() for s in required_skills
#             )

#             skills = [
#                 s for s in skills
#                 if s.lower() in req_set
#             ]

#         # Keyword matching
#         matched_keywords = [
#             k for k in job_keywords
#             if k in resume_text.lower()
#         ]

#         # Score
#         score = len(skills) + len(matched_keywords)

#         # Metadata
#         metadata = extract_metadata(resume_text)

#         result = {
#             "resume_id": i + 1,
#             "filename": resume.get("filename", ""),
#             "uploaded_by": resume.get("uploaded_by", ""),
#             "resume_text": resume_text,
#             "score": score,
#             "matched_skills": skills,
#             "matched_keywords": matched_keywords,
#             "metadata": metadata,
#         }

#         # Per resume analytics
#         result["analytics"] = generate_analytics([result])

#         results.append(result)

#     return sorted(
#         results,
#         key=lambda x: x["score"],
#         reverse=True
#     )


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results, required_skills=None):
#     skill_counts = Counter()
#     keyword_counts = Counter()

#     scores = [r["score"] for r in results]

#     for r in results:

#         for s in r.get("matched_skills", []):
#             skill_counts[s] += 1

#         for k in r.get("matched_keywords", []):
#             keyword_counts[k] += 1

#     return {
#         "skill_distribution": dict(skill_counts),
#         "keyword_distribution": dict(keyword_counts),
#         "scores": scores,
#         "average_score": (
#             sum(scores) / len(scores)
#             if scores else 0
#         ),
#     }


# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# # ---------------- CONTACT ----------------
# def extract_contact(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)

#     return {
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None
#     }


# # ---------------- NAME (ML) ----------------
# def extract_name(text):
#     # Look for "Name: XYZ" format first
#     match = re.search(r'Name[:\-]\s*([A-Za-z ]+)', text)
#     if match:
#         return match.group(1).strip()

#     # fallback: first capitalized full name
#     match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
#     if match:
#         return match.group(1).strip()

#     return None


# # ---------------- SKILLS ----------------
# SKILLS_DB = [
#     "python", "java", "c++", "javascript",
#     "react", "node", "flask", "django",
#     "mongodb", "sql", "docker", "aws"
# ]

# def extract_skills(text):
#     text = text.lower()
#     return [s for s in SKILLS_DB if s in text]


# # ---------------- LINKS ----------------
# def extract_links(text):
#     # URLs
#     github_url = re.search(r'https?://github\.com/[^\s]+', text)
#     linkedin_url = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text)

#     # usernames
#     github_user = re.search(r'GitHub[:\s]+([A-Za-z0-9_-]+)', text, re.IGNORECASE)
#     linkedin_user = re.search(r'LinkedIn[:\s]+([A-Za-z0-9\s_-]+)', text, re.IGNORECASE)

#     github = None
#     linkedin = None

#     if github_url:
#         github = github_url.group(0)
#     elif github_user:
#         username = github_user.group(1).strip()
#         github = f"https://github.com/{username}"

#     if linkedin_url:
#         linkedin = linkedin_url.group(0)
#     elif linkedin_user:
#         name = linkedin_user.group(1).strip().replace(" ", "-")
#         linkedin = f"https://linkedin.com/in/{name}"

#     return {
#         "github": github,
#         "linkedin": linkedin
#     }


# # ---------------- ML RANKING ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):

#     texts = [job_desc] + [r.get("text", "") for r in resumes]

#     vectorizer = TfidfVectorizer(stop_words="english")
#     tfidf = vectorizer.fit_transform(texts)

#     job_vector = tfidf[0]
#     resume_vectors = tfidf[1:]

#     similarities = cosine_similarity(job_vector, resume_vectors)[0]

#     results = []

#     for i, resume in enumerate(resumes):
#         text = resume.get("text", "")

#         name = extract_name(text)
#         contact = extract_contact(text)
#         skills = extract_skills(text)
#         links = extract_links(text)

#         score = float(similarities[i])

#         results.append({
#             "resume_id": i + 1,
#             "filename": resume.get("filename"),
#             "uploaded_by": resume.get("uploaded_by"),

#             "score": score,
#             "name": name,
#             "skills": skills,

#             "email": contact["email"],
#             "phone": contact["phone"],
#             "github": links["github"],
#             "linkedin": links["linkedin"]
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results):
#     scores = [r["score"] for r in results]

#     return {
#         "scores": scores,
#         "average_score": sum(scores) / len(scores) if scores else 0
#     }


# import re

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
#     match = re.search(r'Name[:\-]\s*([A-Za-z ]+)', text)
#     if match:
#         return match.group(1).strip()

#     match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
#     return match.group(1).strip() if match else None


# # ---------------- SKILLS DATABASE ----------------
# SKILLS_DB = [
#     "python", "java", "c++", "javascript",
#     "react", "node", "flask", "django",
#     "mongodb", "sql", "docker", "aws"
# ]


# def extract_skills(text):
#     text = text.lower()
#     return [s for s in SKILLS_DB if s in text]


# # ---------------- LINKS ----------------
# def extract_links(text):
#     github_url = re.search(r'https?://github\.com/[^\s]+', text)
#     linkedin_url = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text)

#     github_user = re.search(r'GitHub[:\s]+([A-Za-z0-9_-]+)', text, re.IGNORECASE)
#     linkedin_user = re.search(r'LinkedIn[:\s]+([A-Za-z0-9\s_-]+)', text, re.IGNORECASE)

#     github = github_url.group(0) if github_url else (
#         f"https://github.com/{github_user.group(1).strip()}" if github_user else None
#     )

#     linkedin = linkedin_url.group(0) if linkedin_url else (
#         f"https://linkedin.com/in/{linkedin_user.group(1).strip().replace(' ', '-')}" if linkedin_user else None
#     )

#     return {"github": github, "linkedin": linkedin}


# # ---------------- MAIN RANKING (SKILL BASED) ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):

#     required_skills = [s.lower() for s in (required_skills or [])]

#     results = []

#     for i, resume in enumerate(resumes):
#         text = resume.get("text", "").lower()

#         resume_skills = extract_skills(text)

#         matched_skills = list(set(required_skills) & set(resume_skills))

#         # ---------------- SCORE LOGIC ----------------
#         if required_skills:
#             skill_score = len(matched_skills) / len(required_skills)
#         else:
#             skill_score = len(resume_skills) / len(SKILLS_DB)

#         # small bonus for overall skill richness
#         richness_bonus = len(resume_skills) / len(SKILLS_DB)

#         score = (skill_score * 0.85) + (richness_bonus * 0.15)

#         results.append({
#             "resume_id": i + 1,
#             "filename": resume.get("filename"),
#             "uploaded_by": resume.get("uploaded_by"),

#             "score": round(score, 4),

#             "matched_skills": matched_skills,
#             "all_skills": resume_skills,

#             "name": extract_name(text),
#             "email": extract_contact(text)["email"],
#             "phone": extract_contact(text)["phone"],
#             "github": extract_links(text)["github"],
#             "linkedin": extract_links(text)["linkedin"]
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results):
#     scores = [r["score"] for r in results]

#     return {
#         "scores": scores,
#         "average_score": round(sum(scores) / len(scores), 4) if scores else 0
#     }


# import re

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
#     match = re.search(r'Name[:\-]\s*([A-Za-z ]+)', text)
#     if match:
#         return match.group(1).strip()

#     match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
#     return match.group(1).strip() if match else None


# # ---------------- SKILLS DB ----------------
# SKILLS_DB = [
#     "python", "java", "c++", "javascript",
#     "react", "node", "flask", "django",
#     "mongodb", "sql", "docker", "aws"
# ]


# def extract_skills(text):
#     text = text.lower()
#     return [s for s in SKILLS_DB if s in text]


# # ---------------- LINKS ----------------
# def extract_links(text):
#     github = re.search(r'https?://github\.com/[^\s]+', text)
#     linkedin = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text)

#     return {
#         "github": github.group(0) if github else None,
#         "linkedin": linkedin.group(0) if linkedin else None
#     }


# # ---------------- NEW SCORING SYSTEM ----------------
# def calculate_score(resume_skills, required_skills):
#     if not required_skills:
#         return 0

#     resume_skills = set([s.lower() for s in resume_skills])
#     required_skills = set([s.lower() for s in required_skills])

#     matched = resume_skills.intersection(required_skills)

#     return round(len(matched) / len(required_skills), 3)


# # ---------------- MAIN RANKING ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):

#     required_skills = [s.lower().strip() for s in (required_skills or [])]

#     job_desc = clean_text(job_desc)

#     texts = [job_desc] + [
#         clean_text(r.get("text", "")) for r in resumes
#     ]

#     vectorizer = TfidfVectorizer(stop_words="english")
#     tfidf = vectorizer.fit_transform(texts)

#     job_vector = tfidf[0]
#     resume_vectors = tfidf[1:]

#     similarities = cosine_similarity(job_vector, resume_vectors)[0]

#     results = []

#     for i, resume in enumerate(resumes):
#         text = clean_text(resume.get("text", ""))

#         skills_found = extract_skills(text)
#         matched_skills = list(set(skills_found) & set(required_skills))

#         # ---------------- SCORE FIX ----------------
#         tfidf_score = float(similarities[i])

#         skill_score = (
#             len(matched_skills) / len(required_skills)
#             if required_skills else 0
#         )

#         # 🔥 BOOST SYSTEM (VERY IMPORTANT FIX)
#         keyword_boost = 0.2 * len(matched_skills)

#         final_score = (
#             0.5 * tfidf_score +
#             0.4 * skill_score +
#             0.1 * keyword_boost
#         )

#         final_score = round(min(final_score, 1), 3)

#         contact = extract_contact(text)
#         links = extract_links(text)

#         results.append({
#             "resume_id": i + 1,
#             "score": final_score,

#             "tfidf_score": float(tfidf_score),
#             "skill_score": float(skill_score),

#             "skills": skills_found,
#             "matched_skills": matched_skills,

#             "email": contact["email"],
#             "phone": contact["phone"],
#             "github": links["github"],
#             "linkedin": links["linkedin"],
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)

# # ---------------- ANALYTICS ----------------
# def generate_analytics(results):
#     scores = [r["score"] for r in results]

#     return {
#         "scores": scores,
#         "average_score": round(sum(scores) / len(scores), 3) if scores else 0
#     }


# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # ---------------- CLEAN TEXT ----------------
# def normalize_text(text):
#     if not text:
#         return ""
#     text = text.lower()
#     text = re.sub(r"[^a-z0-9+.# ]", " ", text)
#     text = re.sub(r"\s+", " ", text)
#     return text.strip()


# # ---------------- CONTACT ----------------
# def extract_contact(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
#     phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)

#     return {
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None
#     }


# # ---------------- LINKS ----------------
# def extract_links(text):
#     github = re.search(r'https?://github\.com/[^\s]+', text)
#     linkedin = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text)

#     return {
#         "github": github.group(0) if github else None,
#         "linkedin": linkedin.group(0) if linkedin else None
#     }


# # ---------------- FIXED SKILL EXTRACTION ----------------
# def extract_skills(text):
#     text = text.lower()
#     found = []

#     skill_map = {
#         "python": ["python"],
#         "flask": ["flask"],
#         "mongodb": ["mongodb", "mongo db"],
#         "sql": ["sql"],
#         "node": ["node", "nodejs", "node.js"],
#         "javascript": ["javascript", "js"],
#         "docker": ["docker"],
#         "aws": ["aws"],
#     }

#     for skill, variants in skill_map.items():
#         if any(v in text for v in variants):
#             found.append(skill)

#     return found


# # ---------------- RANKING ENGINE ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):

#     required_skills = [s.lower().strip() for s in (required_skills or [])]
#     job_desc = normalize_text(job_desc)

#     results = []

#     for i, resume in enumerate(resumes):

#         text = normalize_text(resume.get("text", ""))

#         skills_found = extract_skills(text)

#         matched_skills = list(set(skills_found) & set(required_skills))

#         # ---------------- SKILL SCORE ----------------
#         skill_score = (
#             len(matched_skills) / len(required_skills)
#             if required_skills else 0
#         )

#         # ---------------- TF-IDF SCORE ----------------
#         tfidf_score = 0
#         if len(job_desc.split()) > 2 and len(text.split()) > 5:
#             vectorizer = TfidfVectorizer(stop_words="english")
#             tfidf = vectorizer.fit_transform([job_desc, text])
#             tfidf_score = cosine_similarity(tfidf[0], tfidf[1])[0][0]

#         # ---------------- FINAL SCORE ----------------
#         final_score = round(
#             0.6 * skill_score + 0.4 * tfidf_score,
#             3
#         )

#         contact = extract_contact(text)
#         links = extract_links(text)

#         results.append({
#             "resume_id": i + 1,
#             "score": final_score,

#             "skills": skills_found,
#             "matched_skills": matched_skills,

#             "skill_score": round(skill_score, 3),
#             "tfidf_score": round(tfidf_score, 3),

#             "email": contact["email"],
#             "phone": contact["phone"],
#             "github": links["github"],
#             "linkedin": links["linkedin"],
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results):
#     scores = [r["score"] for r in results]

#     return {
#         "scores": scores,
#         "average_score": round(sum(scores) / len(scores), 3) if scores else 0
#     }


# import re
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# # ---------------- NORMALIZE TEXT ----------------
# def normalize_text(text):
#     if not text:
#         return ""

#     text = text.lower()

#     # normalize common tech variations
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

#     # clean text
#     text = re.sub(r"[^a-z0-9+# ]", " ", text)
#     text = re.sub(r"\s+", " ", text)

#     return text.strip()


# # ---------------- CONTACT EXTRACTION ----------------
# def extract_contact(text):
#     email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)

#     # better phone detection (India-friendly)
#     phone = re.search(r'\b\d{10}\b', text)

#     return {
#         "email": email.group(0) if email else None,
#         "phone": phone.group(0) if phone else None
#     }


# # ---------------- LINKS ----------------
# def extract_links(text):
#     github = re.search(r'https?://github\.com/[^\s]+', text)
#     linkedin = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text)

#     return {
#         "github": github.group(0) if github else None,
#         "linkedin": linkedin.group(0) if linkedin else None
#     }


# # ---------------- SKILL EXTRACTION (UPGRADED) ----------------
# def extract_skills(text):
#     text = normalize_text(text)
#     found = set()

#     skill_keywords = [
#         "python", "java", "c++", "c",
#         "javascript", "js",
#         "nodejs", "expressjs",
#         "react", "nextjs",
#         "mongodb", "sql",
#         "flask", "docker", "aws"
#     ]

#     for skill in skill_keywords:
#         if skill in text:
#             # normalize names
#             if skill == "js":
#                 found.add("javascript")
#             elif skill == "nodejs":
#                 found.add("node")
#             elif skill == "expressjs":
#                 found.add("express")
#             elif skill == "nextjs":
#                 found.add("next")
#             else:
#                 found.add(skill)

#     return list(found)


# # ---------------- RANKING ENGINE ----------------
# def rank_resumes(resumes, job_desc="", required_skills=None):

#     required_skills = [s.lower().strip() for s in (required_skills or [])]
#     job_desc = normalize_text(job_desc)

#     results = []

#     for i, resume in enumerate(resumes):

#         raw_text = resume.get("text", "")
#         text = normalize_text(raw_text)

#         skills_found = extract_skills(text)
#         matched_skills = list(set(skills_found) & set(required_skills))

#         # ---------------- SKILL SCORE ----------------
#         if required_skills:
#             skill_score = len(matched_skills) / len(required_skills)
#         else:
#             # fallback if no required skills
#             skill_score = len(skills_found) / 10

#         # ---------------- TF-IDF SCORE ----------------
#         tfidf_score = 0
#         if len(job_desc.split()) > 3 and len(text.split()) > 10:
#             try:
#                 vectorizer = TfidfVectorizer(stop_words="english")
#                 tfidf = vectorizer.fit_transform([job_desc, text])
#                 tfidf_score = cosine_similarity(tfidf[0], tfidf[1])[0][0]
#             except:
#                 tfidf_score = 0

#         # ---------------- FINAL SCORE ----------------
#         final_score = round(
#             0.6 * skill_score + 0.4 * tfidf_score,
#             3
#         )

#         # fallback fix (prevents 0.000 issue)
#         if final_score == 0 and skills_found:
#             final_score = round(skill_score, 3)

#         contact = extract_contact(raw_text)
#         links = extract_links(raw_text)

#         # ---------------- DEBUG LOG ----------------
#         print("\n--- DEBUG RESUME ---")
#         print("TEXT SAMPLE:", text[:200])
#         print("SKILLS FOUND:", skills_found)
#         print("MATCHED:", matched_skills)
#         print("JOB DESC:", job_desc)
#         print("FINAL SCORE:", final_score)

#         results.append({
#             "resume_id": i + 1,
#             "score": final_score,

#             "skills": skills_found,
#             "matched_skills": matched_skills,

#             "skill_score": round(skill_score, 3),
#             "tfidf_score": round(tfidf_score, 3),

#             "email": contact["email"],
#             "phone": contact["phone"],
#             "github": links["github"],
#             "linkedin": links["linkedin"],
#         })

#     return sorted(results, key=lambda x: x["score"], reverse=True)


# # ---------------- ANALYTICS ----------------
# def generate_analytics(results):
#     scores = [r["score"] for r in results]

#     return {
#         "scores": scores,
#         "average_score": round(sum(scores) / len(scores), 3) if scores else 0
#     }


import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- NORMALIZE TEXT ----------------
def normalize_text(text):
    if not text:
        return ""

    text = text.lower()

    replacements = {
        "node.js": "nodejs",
        "node js": "nodejs",
        "express.js": "expressjs",
        "next.js": "nextjs",
        "react.js": "react",
        "mongo db": "mongodb",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    text = re.sub(r"[^a-z0-9+# ]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------- NORMALIZE SKILL ----------------
def normalize_skill(skill):
    skill = skill.lower().strip()

    mapping = {
        "node": "nodejs",
        "node.js": "nodejs",
        "express": "expressjs",
        "express.js": "expressjs",
        "next": "nextjs",
        "next.js": "nextjs",
        "react.js": "react",
        "mongo db": "mongodb",
    }

    return mapping.get(skill, skill)


# ---------------- CONTACT ----------------
def extract_contact(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'\b\d{10}\b', text)

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None
    }


# ---------------- LINKS ----------------
def extract_links(text):
    github = re.search(r'https?://github\.com/[^\s]+', text)
    linkedin = re.search(r'https?://(www\.)?linkedin\.com/[^\s]+', text)

    return {
        "github": github.group(0) if github else None,
        "linkedin": linkedin.group(0) if linkedin else None
    }


# ---------------- SKILLS ----------------
def extract_skills(text):
    text = normalize_text(text)

    skill_keywords = [
        "python", "java", "c++", "c",
        "javascript",
        "nodejs", "expressjs",
        "react", "nextjs",
        "mongodb", "sql",
        "flask", "docker", "aws"
    ]

    found = set()

    for skill in skill_keywords:
        if skill in text:
            found.add(skill)

    return list(found)


# ---------------- RANKING ----------------
def rank_resumes(resumes, job_desc="", required_skills=None):

    # ✅ normalize required skills HERE (correct place)
    required_skills = [normalize_skill(s) for s in (required_skills or [])]

    job_desc = normalize_text(job_desc)

    results = []

    for i, resume in enumerate(resumes):

        raw_text = resume.get("text", "")
        text = normalize_text(raw_text)

        skills_found = extract_skills(text)

        # ✅ MATCH FIX (NOW WORKS)


        # ---------------- SKILL SCORE ----------------
        if required_skills:
            skill_score = len(matched_skills) / len(required_skills)
        else:
            skill_score = len(skills_found) / 10

        # ---------------- TF-IDF ----------------
        tfidf_score = 0
        if len(job_desc.split()) > 3 and len(text.split()) > 10:
            try:
                vectorizer = TfidfVectorizer(stop_words="english")
                tfidf = vectorizer.fit_transform([job_desc, text])
                tfidf_score = cosine_similarity(tfidf[0], tfidf[1])[0][0]
            except:
                tfidf_score = 0

        # ---------------- FINAL ----------------
        final_score = round(0.6 * skill_score + 0.4 * tfidf_score, 3)

        if final_score == 0 and skills_found:
            final_score = round(skill_score, 3)

        contact = extract_contact(raw_text)
        links = extract_links(raw_text)

        # ✅ DEBUG (KEEP THIS)
        print("\n--- DEBUG ---")
        print("REQUIRED:", required_skills)
        print("FOUND:", skills_found)
        print("MATCHED:", matched_skills)
        print("SCORE:", final_score)

        results.append({
            "resume_id": i + 1,
            "score": final_score,

            "skills": skills_found,
            "matched_skills": matched_skills,

            "skill_score": round(skill_score, 3),
            "tfidf_score": round(tfidf_score, 3),

            "email": contact["email"],
            "phone": contact["phone"],
            "github": links["github"],
            "linkedin": links["linkedin"],
        })

    return sorted(results, key=lambda x: x["score"], reverse=True)


# ---------------- ANALYTICS ----------------
def generate_analytics(results):
    scores = [r["score"] for r in results]

    return {
        "scores": scores,
        "average_score": round(sum(scores) / len(scores), 3) if scores else 0
    }