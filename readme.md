AI Resume Analyzer & ATS System
Developed by: Yash Kapse
An NLP-based web application that analyzes multiple resumes and ranks them against a given Job Description (JD) using Machine Learning and transformer-based semantic models.

Overview
This system simulates an Applicant Tracking System (ATS) by evaluating resumes based on both semantic similarity and skill matching. It leverages Natural Language Processing (NLP) techniques along with transformer-based embeddings to improve matching accuracy.

Key Features
Upload and analyze multiple resumes (PDF format)

Extract and preprocess text using NLP techniques

Rank resumes based on job description relevance

Identify missing skills based on JD requirements

Compute semantic similarity using transformer models (MiniLM)

Hybrid scoring mechanism (semantic + skill-based)

Clean and responsive web interface using Bootstrap

Technologies Used
Backend
Python (Flask)

Natural Language Processing
Tokenization

Lemmatization

Machine Learning & Deep Learning
TF-IDF (baseline comparison)

Sentence Transformers (MiniLM - BERT-based model)

Libraries
NLTK

Scikit-learn

PyPDF2

Sentence-Transformers

System Workflow
User uploads one or more resumes

User inputs a Job Description (JD)

The system performs:

PDF text extraction

Text preprocessing (tokenization and lemmatization)

Semantic similarity computation using transformer embeddings

Skill-based matching

A hybrid score is calculated using:

Semantic similarity score

Skill match score

Resumes are ranked based on the final score

Output
Match percentage for each resume

Ranked list of resumes

Missing skills identified from the Job Description