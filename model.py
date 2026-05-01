import re
from collections import Counter

COMMON_SKILLS = [
    "python","java","c++","javascript","react","node","flask","django",
    "mongodb","sql","docker","aws","git","html","css","typescript",
    "kubernetes","tensorflow","pandas","numpy"
]

# ---------------- METADATA ----------------
def extract_metadata(text):
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'\+?\d[\d -]{8,}\d', text)

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None
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

        if required_skills:
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
        "average_score": sum(scores) / len(scores) if scores else 0
    }