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

    if "project" not in text.lower():
        tips.append("Add projects section")

    if "python" not in text.lower():
        tips.append("Add Python skill")

    if "internship" not in text.lower():
        tips.append("Mention internship experience")

    return tips


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

        return render_template("result.html",
                               score=score,
                               match=match,
                               tips=tips)

    return "No file uploaded"


if __name__ == "__main__":
    app.run(debug=True)