# AI Resume Analyzer & ATS System

### Developed by: Yash Kapse  

An NLP-based web application that analyzes multiple resumes and ranks them against a given Job Description (JD) using Machine Learning and transformer-based semantic models.

---

## Overview

This system simulates an Applicant Tracking System (ATS) by evaluating resumes based on both **semantic similarity** and **skill matching**. It leverages Natural Language Processing (NLP) techniques along with transformer-based embeddings to improve matching accuracy.

---

## Key Features

- Upload and analyze multiple resumes (PDF format)  
- Extract and preprocess text using NLP techniques  
- Rank resumes based on job description relevance  
- Identify missing skills based on JD requirements  
- Compute semantic similarity using transformer models (MiniLM)  
- Hybrid scoring mechanism (semantic + skill-based)  
- Clean and responsive web interface using Bootstrap  

---

## Technologies Used

### Backend
- Python (Flask)

### Natural Language Processing
- Tokenization  
- Lemmatization  

### Machine Learning & Deep Learning
- TF-IDF (baseline comparison)  
- Sentence Transformers (MiniLM - BERT-based model)  

### Libraries
- NLTK  
- Scikit-learn  
- PyPDF2  
- Sentence-Transformers  

---

## System Workflow

1. User uploads one or more resumes  
2. User inputs a Job Description (JD)  
3. The system performs:
   - PDF text extraction  
   - Text preprocessing (tokenization and lemmatization)  
   - Semantic similarity computation using transformer embeddings  
   - Skill-based matching  
4. A hybrid score is calculated using:
   - Semantic similarity score  
   - Skill match score  
5. Resumes are ranked based on the final score  

---

## Output

- Match percentage for each resume  
- Ranked list of resumes  
- Missing skills identified from the Job Description  

---

## Project Structure

```
ai-resume-analyzer-ats/
│
├── app.py
├── templates/
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
├── uploads/
├── README.md
```

---

## Installation and Setup

### 1. Clone the Repository
```
git clone https://github.com/your-username/ai-resume-analyzer-ats.git
cd ai-resume-analyzer-ats
```

### 2. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```
pip install flask nltk scikit-learn PyPDF2 sentence-transformers
```

### 4. Run the Application
```
python app.py
```

---

## Usage

1. Open browser at: `http://127.0.0.1:5000`  
2. Upload one or more resumes  
3. Paste the job description  
4. Click on "Analyze & Rank"  
5. View ranked results with match scores and missing skills  

---

## Future Enhancements

- Resume summary generation using AI  
- Automatic skill extraction from job descriptions (NER)  
- Downloadable analysis reports (PDF)  
- Deployment as a SaaS platform  

---

## Viva Explanation

This system uses NLP preprocessing techniques such as tokenization and lemmatization, along with transformer-based sentence embeddings, to compute semantic similarity between resumes and job descriptions. A hybrid scoring approach combining semantic similarity and skill-based matching is used to simulate real-world ATS systems.