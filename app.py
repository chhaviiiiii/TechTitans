from flask import Flask, request, jsonify
import os
import logging
from resume_parser import extract_text
from feedback_engine import generate_feedback
import psycopg2

app = Flask(__name__)

# -------- FOLDERS --------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs("logs", exist_ok=True)

# -------- LOGGING --------
logging.basicConfig(
    filename="logs/errors.txt",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -------- DATABASE --------
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Hackathon",
        user="postgres",
        password="qwer1234"
    )

# -------- ROUTE --------
@app.route("/upload", methods=["POST"])
def upload_resume():
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        text = extract_text(file_path)
        feedback = generate_feedback(text)

        return jsonify({"feedback": feedback})

    except Exception as e:
        logging.error(str(e))
        return jsonify({"error": "Something went wrong"}), 500
print("Upload endpoint hit")

# -------- RUN --------
if __name__ == "__main__":
    app.run(debug=True)