import re
import psycopg2
from minio_config import connect_db

# Define broad keyword patterns for extraction
SKILL_KEYWORDS = [
    "java", "python", "c++", "c#", "javascript", "react", "angular", "node.js", "sql", "postgresql",
    "mongodb", "machine learning", "deep learning", "artificial intelligence", "nlp", "data science",
    "devops", "aws", "azure", "docker", "kubernetes", "tensorflow", "pytorch", "html", "css", "django", "flask"
]
EDUCATION_KEYWORDS = ["bachelor", "master", "b.tech", "b.e", "m.tech", "phd", "bsc", "msc", "diploma"]
EXPERIENCE_KEYWORDS = ["experience", "worked at", "internship", "company", "role", "position"]
CERTIFICATION_KEYWORDS = ["certified", "certification", "course", "training"]
PROJECT_KEYWORDS = ["project", "developed", "implemented", "created"]
ACHIEVEMENT_KEYWORDS = ["award", "achievement", "won", "scholarship", "honor"]

def extract_information(resume_text):
    """
    Extracts structured information from resume text.
    """
    extracted_info = {
        "name": "",
        "email": "",
        "phone": "",
        "skills": [],
        "education": [],
        "experience": [],
        "certifications": [],
        "projects": [],
        "achievements": []
    }

    # Extract email
    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", resume_text)
    if email_match:
        extracted_info["email"] = email_match.group()

    # Extract phone number
    phone_match = re.search(r"\b\d{10}\b", resume_text)
    if phone_match:
        extracted_info["phone"] = phone_match.group()

    # Extract skills
    extracted_info["skills"] = [skill for skill in SKILL_KEYWORDS if skill.lower() in resume_text.lower()]

    # Extract education
    extracted_info["education"] = [edu for edu in EDUCATION_KEYWORDS if edu.lower() in resume_text.lower()]

    # Extract experience
    extracted_info["experience"] = [exp for exp in EXPERIENCE_KEYWORDS if exp.lower() in resume_text.lower()]

    # Extract certifications
    extracted_info["certifications"] = [cert for cert in CERTIFICATION_KEYWORDS if cert.lower() in resume_text.lower()]

    # Extract projects
    extracted_info["projects"] = [proj for proj in PROJECT_KEYWORDS if proj.lower() in resume_text.lower()]

    # Extract achievements
    extracted_info["achievements"] = [ach for ach in ACHIEVEMENT_KEYWORDS if ach.lower() in resume_text.lower()]

    return extracted_info

def update_database(user_id, extracted_info):
    """
    Updates PostgreSQL database with extracted resume details.
    """
    conn = connect_db()
    cur = conn.cursor()

    update_fields = []
    update_values = []

    for field, value in extracted_info.items():
        if value:  # Only update non-empty fields
            if isinstance(value, list):
                value = ", ".join(value)
            update_fields.append(f"{field} = %s")
            update_values.append(value)

    if update_fields:
        sql_query = f"""
        UPDATE users
        SET {", ".join(update_fields)}
        WHERE id = %s;
        """
        update_values.append(user_id)

        cur.execute(sql_query, update_values)
        conn.commit()
        print(f"✅ Successfully updated user {user_id} with extracted resume info.")

    cur.close()
    conn.close()

def process_resumes():
    """
    Fetches resumes from database, extracts details, and updates user records.
    """
    conn = connect_db()
    cur = conn.cursor()

    # Fetch users with resume text
    cur.execute("SELECT id, resume_text FROM users WHERE resume_text IS NOT NULL;")
    users = cur.fetchall()

    if not users:
        print("❌ No resumes found in the database.")
        return

    for user_id, resume_text in users:
        print(f"🔍 Processing resume for User ID: {user_id}")
        extracted_info = extract_information(resume_text)
        update_database(user_id, extracted_info)

    cur.close()
    conn.close()

if __name__ == "__main__":
    process_resumes()
