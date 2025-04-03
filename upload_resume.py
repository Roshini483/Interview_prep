from minio import Minio
import psycopg2
import os

# MinIO Configuration
minio_client = Minio(
    "127.0.0.1:9001",  # MinIO address
    access_key="roshini",  # Your MinIO username
    secret_key="sushma2006",  # Your MinIO password
    secure=False  # Change to True if using HTTPS
)

bucket_name = "resumes"  # Ensure this bucket exists

# Function to upload resume
def upload_resume(user_id, file_path, file_name):
    """Uploads a resume to MinIO and returns the file URL."""
    try:
        if not os.path.exists(file_path):
            print(f"❌ Error: File not found at {file_path}")
            return None

        minio_client.fput_object(bucket_name, file_name, file_path)
        resume_url = f"http://127.0.0.1:9001/{bucket_name}/{file_name}"
        print(f"✅ Resume uploaded successfully! URL: {resume_url}")
        return resume_url
    except Exception as e:
        print(f"❌ Error uploading resume: {e}")
        return None

# Function to store resume URL in PostgreSQL
def store_resume_url(user_id, resume_url):
    """Stores the generated resume URL in the PostgreSQL database for the given user."""
    try:
        conn = psycopg2.connect(
            dbname="interview_prep",  # Change to your database name
            user="postgres",  # Change to your PostgreSQL username
            password="roshini2006",  # Change to your PostgreSQL password
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        sql = "UPDATE users SET resume_url = %s WHERE id = %s"
        cur.execute(sql, (resume_url, user_id))
        conn.commit()
        cur.close()
        conn.close()
        print(f"✅ Resume URL stored in database for user {user_id}: {resume_url}")
    except Exception as e:
        print(f"❌ Error storing resume URL in database: {e}")

# Example usage
if __name__ == "__main__":
    user_id = 1  # Change this to a valid user ID from your database
    file_path = "C:\\Users\\roshi\\Downloads\\resume1.pdf"  # Path to your resume file
    file_name = "resume1.pdf"  # Unique filename

    resume_url = upload_resume(user_id, file_path, file_name)
    if resume_url:
        store_resume_url(user_id, resume_url)

