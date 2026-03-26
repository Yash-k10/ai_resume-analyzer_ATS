from flask import Flask, render_template, request
import os
import PyPDF2

app = Flask(__name__)

# Upload folder setup
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure uploads folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🔥 ATS Score Function (upar hona chahiye)
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


# 🔥 PDF → Text Extraction Function
def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    return text


# 🏠 Home Route
@app.route("/")
def home():
    return render_template("index.html")


# 📤 Upload Route
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]

    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # 🔥 Extract text from PDF
        text = extract_text(filepath)

        # 🔥 Calculate ATS Score
        score = ats_score(text)

        return f"""
        <h2>ATS Score: {score}/100</h2>
        <h3>Extracted Text Preview:</h3>
        <p>{text[:500]}</p>
        """

    return "No file uploaded"


# ▶️ Run App
if __name__ == "__main__":
    app.run(debug=True)