import psycopg2
import fitz  # PyMuPDF for text-based PDFs
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np

# PostgreSQL Configuration
DB_CONFIG = {
    "dbname": "interview_prep",
    "user": "postgres",
    "password": "roshini2006",
    "host": "localhost",
    "port": "5432"
}

# Tesseract Path (Update if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF, handling both text-based and scanned PDFs."""
    full_text = ""

    try:
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            text = doc[page_num].get_text("text")
            if text.strip():  # If text is detected, add it
                full_text += text + "\n"
            else:  # If no text, treat it as a scanned image
                pix = doc[page_num].get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Convert image to OpenCV format
                img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
                _, img_thresh = cv2.threshold(img_cv, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # OCR Extraction
                ocr_text = pytesseract.image_to_string(img_thresh)
                full_text += ocr_text + "\n"

        return full_text.strip()

    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return None

def store_resume_data(user_id, extracted_text):
    """Stores full extracted resume text in PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        query = """
        UPDATE users 
        SET resume_text = %s
        WHERE id = %s
        """
        cur.execute(query, (extracted_text, user_id))

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Full Resume Text Stored in PostgreSQL Successfully!")

    except Exception as e:
        print(f"❌ Error storing resume text: {e}")

if __name__ == "__main__":
    user_id = 1  # Change to the actual user ID
    pdf_path = "C:\\Users\\roshi\\Downloads\\resume1.pdf"  # Change to your resume file path

    extracted_text = extract_text_from_pdf(pdf_path)  # Full extracted text
    if extracted_text:
        print("\n✅ Extracted Resume Text:")
        print(extracted_text)
        
        store_resume_data(user_id, extracted_text)
    else:
        print("❌ Failed to extract text from resume.")

