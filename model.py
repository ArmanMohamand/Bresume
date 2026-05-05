import re
from collections import Counter

COMMON_SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "react",
    "node",
    "flask",
    "django",
    "mongodb",
    "sql",
    "docker",
    "aws",
    "git",
    "html",
    "css",
    "typescript",
    "kubernetes",
    "tensorflow",
    "pandas",
    "numpy",
]

# ---------------- METADATA ----------------
def extract_metadata(text):
    # Email + phone
    email = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    phone = re.search(r'\+?\d[\d\s-]{8,}\d', text)

    # GitHub
    github = re.search(
        r'(https?://github\.com/[^\s]+|GitHub:\s*[A-Za-z0-9_-]+)',
        text,
        re.IGNORECASE
    )

    # LinkedIn
    linkedin = re.search(
        r'(https?://(www\.)?linkedin\.com/[^\s]+|LinkedIn:\s*[A-Za-z0-9_-]+)',
        text,
        re.IGNORECASE
    )

    # Name
    name_match = re.search(r'Name[:\-]\s*(.*)', text)

    if not name_match:
        name_match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)

    # Projects
    projects_section = re.findall(
        r'Projects?\s*[\n\r]+([\s\S]+?)(?=\n\n|$)',
        text,
        re.IGNORECASE
    )

    projects = []
    project_links = []

    if projects_section:
        for line in projects_section[0].splitlines():
            line = line.strip()

            if line and not line.lower().startswith("projects"):
                projects.append(line)

                url_match = re.search(r'https?://[^\s\)]+', line)

                if url_match:
                    project_links.append(url_match.group(0))

    return {
        "name": name_match.group(1).strip() if name_match else None,
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None,
        "github": github.group(0) if github else None,
        "linkedin": linkedin.group(0) if linkedin else None,
        "projects": projects,
        "project_links": project_links,
    }


# ---------------- SKILL EXTRACTION ----------------
def extract_skills(text):
    if not text:
        return []

    text = text.lower()

    return [s for s in COMMON_SKILLS if s in text]


# ---------------- RANKING ----------------
def rank_resumes(resumes, job_desc="", required_skills=None):
    job_keywords = set(
        re.findall(r'\w+', job_desc.lower())
    )

    results = []

    for i, resume in enumerate(resumes):

        # ✅ FIX: resume is dictionary
        resume_text = resume.get("text", "")

        if not isinstance(resume_text, str):
            resume_text = str(resume_text)

        # Extract skills
        skills = extract_skills(resume_text)

        # Filter required skills
        if required_skills and len(required_skills) > 0:
            req_set = set(
                s.lower() for s in required_skills
            )

            skills = [
                s for s in skills
                if s.lower() in req_set
            ]

        # Keyword matching
        matched_keywords = [
            k for k in job_keywords
            if k in resume_text.lower()
        ]

        # Score
        score = len(skills) + len(matched_keywords)

        # Metadata
        metadata = extract_metadata(resume_text)

        result = {
            "resume_id": i + 1,
            "filename": resume.get("filename", ""),
            "uploaded_by": resume.get("uploaded_by", ""),
            "resume_text": resume_text,
            "score": score,
            "matched_skills": skills,
            "matched_keywords": matched_keywords,
            "metadata": metadata,
        }

        # Per resume analytics
        result["analytics"] = generate_analytics([result])

        results.append(result)

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )


# ---------------- ANALYTICS ----------------
def generate_analytics(results, required_skills=None):
    skill_counts = Counter()
    keyword_counts = Counter()

    scores = [r["score"] for r in results]

    for r in results:

        for s in r.get("matched_skills", []):
            skill_counts[s] += 1

        for k in r.get("matched_keywords", []):
            keyword_counts[k] += 1

    return {
        "skill_distribution": dict(skill_counts),
        "keyword_distribution": dict(keyword_counts),
        "scores": scores,
        "average_score": (
            sum(scores) / len(scores)
            if scores else 0
        ),
    }