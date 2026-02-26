from flask import Flask, request, jsonify
from dbtest import get_connection
import json
import random

app = Flask(__name__)

@app.route("/generate_questions", methods=["POST"])
def generate_questions():
    data = request.json

    resume_id = data["resume_id"]
    domain = data["domain"]
    experience = data["experience"]

    # 1️⃣ Get resume from DB
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT parsed_json FROM resumes WHERE id = %s;", (resume_id,))
    result = cur.fetchone()

    cur.close()
    conn.close()

    if not result:
        return jsonify({"error": "Resume not found"}), 404

    parsed_data = result[0]  # JSONB auto dict me aata hai

    skills = parsed_data.get("skills", [])

    # 2️⃣ Question Generator Logic
    questions = []

    for skill in skills:
        questions.append(f"Explain your experience with {skill}.")
        questions.append(f"What challenges did you face while working with {skill}?")

    # Domain specific
    if domain.lower() == "web development":
        questions.append("What is REST API?")
        questions.append("Difference between frontend and backend?")

    if domain.lower() == "machine learning":
        questions.append("Explain bias vs variance.")
        questions.append("What is overfitting?")

    # Experience based
    if experience.lower() == "fresher":
        questions.append("Explain one academic project in detail.")
    else:
        questions.append("Describe a real-world production problem you solved.")

    # Shuffle and limit to 5
    random.shuffle(questions)
    final_questions = questions[:5]

    return jsonify({
        "questions": final_questions
    })