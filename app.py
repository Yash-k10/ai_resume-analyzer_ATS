from flask import Flask, render_template, request
import os
import PyPDF2
import nltk

from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util

# NLTK setup
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

lemmatizer = WordNetLemmatizer()

# 🔥 Load AI model (once)
model = SentenceTransformer('all-MiniLM-L6-v2')


# 🔹 Preprocess
def preprocess(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(w) for w in tokens if w.isalnum()]
    return " ".join(tokens)


# 🔹 Extract PDF
def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# 🔹 Skill List (important)
skills_list = [
    "python", "sql", "machine learning", "deep learning",
    "nlp", "flask", "django", "react", "api", "aws",
    "docker", "tensorflow", "pandas", "numpy"
]


# 🔹 Skill Score
def skill_score(resume, jd):
    match = 0
    total = 0

    for skill in skills_list:
        if skill in jd:
            total += 1
            if skill in resume:
                match += 1

    return (match / total) if total != 0 else 0


# 🔹 🔥 BERT Semantic Score
def semantic_score(resume, jd):
    emb1 = model.encode(resume, convert_to_tensor=True)
    emb2 = model.encode(jd, convert_to_tensor=True)

    sim = util.cos_sim(emb1, emb2)
    return sim.item()


# 🔹 🔥 FINAL HYBRID SCORE
def final_score(resume, jd):
    sem = semantic_score(resume, jd)
    skill = skill_score(resume, jd)

    # weighted combination
    final = (0.7 * sem) + (0.3 * skill)

    return round(final * 100, 2)


# 🔹 Missing Skills
def missing_skills(resume, jd):
    missing = []
    for skill in skills_list:
        if skill in jd and skill not in resume:
            missing.append(skill)
    return missing


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("resume")
    jd = request.form.get("jd")

    results = []

    clean_jd = preprocess(jd) if jd else ""

    for file in files:
        if file:
            path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(path)

            text = extract_text(path)
            clean_text = preprocess(text)

            score = final_score(clean_text, clean_jd)
            missing = missing_skills(clean_text, clean_jd)

            results.append({
                "name": file.filename,
                "match": score,
                "missing": missing
            })

    # 🔥 Rank properly
    results = sorted(results, key=lambda x: x["match"], reverse=True)

    return render_template("result.html", results=results)


if __name__ == "__main__":
    app.run(debug=True)