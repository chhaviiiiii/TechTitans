import re

def generate_feedback(text):

    text_lower = text.lower()

    strengths = []
    weaknesses = []
    score = 50
    role = "General Developer"

    # -------- ROLE DETECTION --------
    if "java" in text_lower:
        role = "Java Developer"
    elif "flutter" in text_lower or "dart" in text_lower:
        role = "Flutter Developer"
    elif "python" in text_lower:
        role = "Python Developer"
    elif "database" in text_lower or "sql" in text_lower or "mysql" in text_lower:
        role = "Database Administrator"

    # -------- COMMON CHECKS --------
    if "%" in text or "improved" in text_lower:
        strengths.append("Quantified achievements found.")
        score += 10
    else:
        weaknesses.append("No quantified achievements mentioned.")

    if len(text) < 800:
        weaknesses.append("Resume seems too short.")
        score -= 5

    if "objective" not in text_lower:
        weaknesses.append("No clear objective statement.")

    # -------- ROLE SPECIFIC LOGIC --------

    if role == "Java Developer":
        if "spring" in text_lower or "spring boot" in text_lower:
            strengths.append("Spring/Spring Boot experience detected.")
            score += 10
        else:
            weaknesses.append("Spring Boot experience not highlighted.")

        if "rest" in text_lower or "api" in text_lower:
            strengths.append("REST API development mentioned.")
            score += 5

    elif role == "Flutter Developer":
        if "dart" in text_lower:
            strengths.append("Strong Dart knowledge detected.")
            score += 10
        if "firebase" in text_lower:
            strengths.append("Firebase integration experience found.")
            score += 5
        else:
            weaknesses.append("Firebase or backend integration not mentioned.")

    elif role == "Python Developer":
        if "django" in text_lower or "flask" in text_lower:
            strengths.append("Backend framework experience detected.")
            score += 10
        if "machine learning" in text_lower or "ai" in text_lower:
            strengths.append("AI/ML experience mentioned.")
            score += 5

    elif role == "Database Administrator":
        if "mysql" in text_lower or "postgres" in text_lower:
            strengths.append("Database management experience found.")
            score += 10
        if "performance tuning" in text_lower:
            strengths.append("Performance tuning experience mentioned.")
            score += 5
        else:
            weaknesses.append("Database optimization experience not highlighted.")

    score = min(score, 95)

    feedback = f"""
===== AI RESUME FEEDBACK =====

Detected Role: {role}

Strengths:
- {'\n- '.join(strengths) if strengths else "Basic structure detected."}

Weaknesses:
- {'\n- '.join(weaknesses) if weaknesses else "Minor improvements needed."}

ATS Score: {score}/100

Suggestions:
- Add measurable achievements with numbers.
- Highlight relevant tech stack clearly.
- Use strong action verbs.
- Keep formatting clean and consistent.
"""

    return feedback