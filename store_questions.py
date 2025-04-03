from minio_config import connect_db  

def store_question(user_id, question_text, category, difficulty):
    """
    Stores an AI-generated question in the questions table.
    
    Parameters:
        user_id (int): ID of the user for whom the question is generated.
        question_text (str): The AI-generated question text.
        category (str): The category of the question (e.g., "Technical", "Behavioral").
        difficulty (str): The difficulty level (e.g., "Easy", "Medium", "Hard").
    """
    try:
        conn = connect_db()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO questions (user_id, question_text, category, difficulty, generated_at)
            VALUES (%s, %s, %s, %s, NOW());
        """, (user_id, question_text, category, difficulty))
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"✅ Question stored successfully for User ID: {user_id}")

    except Exception as e:
        print(f"❌ Error storing question: {e}")

