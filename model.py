import re
from collections import Counter

COMMON_SKILLS = [
    "python","java","c++","javascript","react","node","flask","django",
    "mongodb","sql","docker","aws","git","html","css","typescript",
    "kubernetes","tensorflow","pandas","numpy"
]

def extract_metadata(text):
    """Extract email, phone, and name from resume text"""
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone_match = re.search(r'\+?\d[\d -]{8,}\d', text)

    # crude name extraction: first non-empty line with capitalized words
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    name = None
    if lines:
        first_line = lines[0]
        if re.match(r'^[A-Z][a-z]+(\s[A-Z][a-z]+)*$', first_line):
            name = first_line

    return {
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0) if phone_match else None,
        "name": name
    }

def extract_skills(text):
    text_lower = text.lower()
    return [skill.capitalize() for skill in COMMON_SKILLS if skill in text_lower]

def rank_resumes(resumes, job_desc="", required_skills=None):
    job_keywords = set(job_desc.lower().split())
    results = []
    for i, resume in enumerate(resumes):
        auto_skills = extract_skills(resume)
        matched_skills = auto_skills
        if required_skills:
            matched_skills = [s for s in auto_skills if s.lower() in [rs.lower() for rs in required_skills]]
        matched_keywords = [kw for kw in job_keywords if kw in resume.lower()]
        score = len(matched_skills) + len(matched_keywords)
        results.append({
            "resume_id": i + 1,
            "resume_text": resume,
            "score": score,
            "matched_skills": matched_skills,
            "matched_keywords": matched_keywords
        })
    results.sort(key=lambda r: r["score"], reverse=True)
    return results

def generate_analytics(results, required_skills=None):
    skill_counts = Counter()
    keyword_counts = Counter()
    scores = [r["score"] for r in results]

    for r in results:
        for skill in r["matched_skills"]:
            skill_counts[skill] += 1
        for kw in r.get("matched_keywords", []):
            keyword_counts[kw] += 1

    return {
        "skill_distribution": dict(skill_counts),
        "keyword_distribution": dict(keyword_counts),
        "average_score": sum(scores) / len(scores) if scores else 0,
        "scores": scores,
        "required_skills": required_skills or []
    }
