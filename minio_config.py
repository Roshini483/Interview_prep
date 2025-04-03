from minio import Minio
import psycopg2

# MinIO Configuration
MINIO_URL = "localhost:9000"  # Change if MinIO is running remotely
MINIO_ACCESS_KEY = "roshini"  # Your MinIO username
MINIO_SECRET_KEY = "sushma2006"  # Your MinIO password
BUCKET_NAME = "resumes"  # Name of your MinIO bucket

# PostgreSQL Configuration
DB_NAME = "interview_prep"
DB_USER = "your_db_user"  # Change to your PostgreSQL username
DB_PASSWORD = "your_db_password"  # Change to your PostgreSQL password
DB_HOST = "localhost"
DB_PORT = "5432"

# Initialize MinIO Client
minio_client = Minio(
    MINIO_URL,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Function to get PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="interview_prep",
        user="postgres",
        password="roshini2006",
        host="localhost",  # Change if your database is hosted elsewhere
        port="5432"  # Default PostgreSQL port
    )
