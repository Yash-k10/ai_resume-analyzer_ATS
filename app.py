from flask import Flask, render_template, request
import os
import PyPDF2

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔹 ATS Score
def ats_score(text):
    keywords = [
        "python", "machine learning", "data analysis",
        "sql", "project", "internship", "deep learning"
    ]

    score = 0
    text = text.lower()

    for word in keywords:
        if word in text:
            score += 100 / len(keywords)

    return round(score, 2)


# 🔹 PDF → Text
def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# 🔹 JD Matching
def match_score(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_text, jd_text])
    similarity = cosine_similarity(vectors[0], vectors[1])
    return round(similarity[0][0] * 100, 2)


# 🔹 Suggestions
def suggestions(text):
    tips = []
    text = text.lower()

    if "project" not in text:
        tips.append("Add projects section")

    if "python" not in text:
        tips.append("Add Python skill")

    if "internship" not in text:
        tips.append("Mention internship experience")

    return tips


# 🔹 Strong Points
def strong_points(text):
    strengths = []
    text = text.lower()

    if "python" in text:
        strengths.append("Good knowledge of Python")

    if "machine learning" in text:
        strengths.append("Machine Learning experience")

    if "project" in text:
        strengths.append("Project experience present")

    if "internship" in text:
        strengths.append("Has internship experience")

    return strengths


# 🔹 Missing Skills
def missing_skills(resume_text, jd_text):
    if not jd_text:
        return []

    resume_text = resume_text.lower()
    jd_text = jd_text.lower()

    # ❌ Ignore useless words
    ignore_words = [
        "and", "the", "with", "for", "you", "are", "job", "role",
        "title", "description", "experience", "years", "location",
        "remote", "hybrid", "work", "team", "good", "skills"
    ]

    # ✅ Important skill keywords (customizable 🔥)
    skill_keywords = [
        "python", "java", "sql", "machine learning", "deep learning",
        "data analysis", "nlp", "tensorflow", "pandas", "numpy",
        "flask", "django", "react", "node", "api", "docker", "aws"
    ]

    missing = []

    # 🔍 Check only important skills
    for skill in skill_keywords:
        if skill in jd_text and skill not in resume_text:
            missing.append(skill)

    return missing


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]
    jd = request.form.get("jd")

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        text = extract_text(filepath)

        score = ats_score(text)

        match = 0
        if jd:
            match = match_score(text, jd)

        tips = suggestions(text)
        strengths = strong_points(text)
        missing = missing_skills(text, jd)

        return render_template("result.html",
                               score=score,
                               match=match,
                               tips=tips,
                               strengths=strengths,
                               missing=missing)

    return "No file uploaded"


if __name__ == "__main__":
    app.run(debug=True)