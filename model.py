import re

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

    text = re.sub(r"[^a-z0-9+#:/._ -]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------- CONTACT ----------------
def extract_contact(text):

    email = re.search(
        r'[\w\.-]+@[\w\.-]+\.\w+',
        text
    )

    phone = re.search(
        r'\b\d{10}\b',
        text
    )

    return {
        "email": email.group(0) if email else None,
        "phone": phone.group(0) if phone else None
    }


# ---------------- LINKS ----------------
def extract_links(text):

    # github full url
    github = re.search(
        r'(https?://)?(www\.)?github\.com/[a-zA-Z0-9_-]+',
        text,
        re.IGNORECASE
    )

    # linkedin full url only
    linkedin = re.search(
        r'(https?://)?(www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+',
        text,
        re.IGNORECASE
    )

    github_url = github.group(0) if github else None
    linkedin_url = linkedin.group(0) if linkedin else None

    # github username fallback
    if not github_url:

        github_name = re.search(
            r'github\s*:?\s*([a-zA-Z0-9_-]+)',
            text,
            re.IGNORECASE
        )

        if github_name:
            github_url = (
                f"https://github.com/{github_name.group(1)}"
            )

    # add https if missing
    if github_url and not github_url.startswith("http"):
        github_url = "https://" + github_url

    if linkedin_url and not linkedin_url.startswith("http"):
        linkedin_url = "https://" + linkedin_url

    return {
        "github": github_url,
        "linkedin": linkedin_url
    }


# ---------------- PROJECTS ----------------
def extract_projects(text):

    projects = []
    project_links = []

    lines = text.split("\n")

    for line in lines:

        clean_line = line.strip()

        # detect project titles
        if any(keyword in clean_line.lower() for keyword in [
            "project",
            "system",
            "website",
            "app",
            "management"
        ]):

            if 10 < len(clean_line) < 200:
                projects.append(clean_line)

        # detect urls
        urls = re.findall(
            r'https?://[^\s]+',
            clean_line
        )

        for url in urls:

            if (
                "linkedin.com" not in url
                and "github.com" not in url
            ):
                project_links.append(url)

    projects = list(dict.fromkeys(projects))[:5]

    project_links = list(
        dict.fromkeys(project_links)
    )[:5]

    return {
        "projects": projects,
        "project_links": project_links
    }


# ---------------- SKILLS ----------------
def extract_skills(text):

    text = normalize_text(text)

    skill_keywords = [

        # languages
        "python",
        "java",
        "c++",
        "c",
        "javascript",
        "typescript",

        # frontend
        "react",
        "nextjs",
        "vue",
        "angular",
        "tailwind",
        "bootstrap",
        "html",
        "css",
        "vite",

        # backend
        "nodejs",
        "expressjs",
        "flask",
        "django",

        # database
        "mongodb",
        "sql",
        "mysql",
        "postgresql",

        # tools
        "docker",
        "aws",
        "git",
        "github",
        "vercel",
        "render",

        # concepts
        "dsa",
        "rest",
        "jwt",
        "api"
    ]

    found = []

    for skill in skill_keywords:

        if skill == "c":

            if re.search(r'\bc\b', text):
                found.append(skill)

        elif re.search(
            rf'\b{re.escape(skill)}\b',
            text
        ):
            found.append(skill)

    # smart dsa detection
    if (
        "data structure" in text
        or "algorithms" in text
    ):

        if "dsa" not in found:
            found.append("dsa")

    return list(dict.fromkeys(found))


# ---------------- METADATA ----------------
# ---------------- METADATA ----------------
def extract_metadata(
    text,
    username=None,
    custom_linkedin=None,
    custom_github=None,
    custom_project_links=None
):

    contact = extract_contact(text)

    links = extract_links(text)

    projects = extract_projects(text)

    github = links["github"]


    linkedin = (
        custom_linkedin
        if custom_linkedin
        else links["linkedin"]
    )

    project_links = (
        custom_project_links
        if custom_project_links
        else projects["project_links"]
    )

    return {

        "name": username,

        "email": contact["email"],

        "phone": contact["phone"],

        "github": github,

        "linkedin": linkedin,

        "projects": projects["projects"],

        "project_links": project_links
    }
# ---------------- RANK RESUMES ----------------
def rank_resumes(
    resumes,
    job_desc="",
    required_skills=None,
    current_user_email=None
):

    results = []

    for i, resume in enumerate(resumes):

        raw_text = resume.get("text", "")

        username = resume.get("username", "Unknown")

        filename = resume.get("filename", "Resume.pdf")

        metadata = extract_metadata(
            raw_text,
            username,
                resume.get("linkedin"),

    resume.get("github"),

    resume.get("project_links", [])

        )

        skills_found = extract_skills(raw_text)

        # score = number of skills
        final_score = len(skills_found)

        # own resume first
        if metadata["email"] == current_user_email:
            final_score += 1000

        result = {

            # IMPORTANT
            "resume_id": resume.get("id", i + 1),

            # NEW
            "filename": filename,

            "score": final_score,

            "skills": skills_found,

            "email": metadata["email"],

            "phone": metadata["phone"],

            "github": metadata["github"],

            "linkedin": metadata["linkedin"],

            "metadata": metadata
        }

        results.append(result)

    return sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

# ---------------- ANALYTICS ----------------
def generate_analytics(results):

    scores = [r["score"] for r in results]

    return {
        "scores": scores,
        "average_score": round(
            sum(scores) / len(scores),
            3
        ) if scores else 0
    }