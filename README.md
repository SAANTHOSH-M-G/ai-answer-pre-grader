# AI Answer Pre-Grader

AI-assisted handwritten examination answer pre-grading using OCR, Qwen3, rubric-based evaluation, and teacher review.

## Overview

This project converts a handwritten student answer sheet into structured answers and generates rubric-based **suggested marks** using a locally running Qwen3 model.

The system is designed as an **AI-assisted pre-grader**, not an autonomous grading system. The teacher always has the final authority over the marks.

## Workflow

```text
Teacher Question + Answer Key + Rubric
                 |
                 v
       Handwritten Answer Sheet
                 |
                 v
             EasyOCR
                 |
                 v
          Extracted OCR Text
                 |
                 v
        Qwen3 Answer Structuring
                 |
                 v
      Rubric-Based Qwen3 Evaluation
                 |
                 v
 Suggested Marks + Evidence + Confidence
                 |
                 v
          Teacher Review
                 |
                 v
           Final Score
```

## Features

- Handwritten answer-sheet OCR using EasyOCR
- Automatic separation of answers by question
- Local Qwen3 8B inference through Ollama
- Rubric-by-rubric evaluation
- Suggested score and maximum score
- Evidence for each rubric criterion
- Confidence score
- Missing-concept detection
- Automatic manual-review flag for uncertain cases
- Multiple exam questions
- Teacher final review and finalization
- Local processing architecture

## Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, Flask, Flask-CORS
- **OCR:** EasyOCR
- **LLM:** Qwen3 8B
- **LLM Runtime:** Ollama
- **HTTP/API:** REST-style Flask endpoints

## Project Structure

```text
answer-pre-grader/
|
├── backend/
│   ├── app.py
│   ├── ocr.py
│   ├── parser.py
│   └── grader.py
|
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
|
├── tests/
|
├── requirements.txt
├── .gitignore
└── README.md
```

## Requirements

- Windows, Linux, or macOS
- Python 3.10+
- Ollama
- Qwen3 8B model
- Enough RAM/storage for local OCR and LLM inference

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/SAANTHOSH-M-G/ai-answer-pre-grader.git
cd ai-answer-pre-grader
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.env\Scripts\Activate.ps1
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install and start Qwen3 with Ollama

```bash
ollama pull qwen3:8b
```

Make sure Ollama is running before using the application.

### 5. Start the Flask backend

```bash
cd backend
python app.py
```

The backend runs at:

```text
http://127.0.0.1:5000
```

### 6. Start the frontend

Open another terminal:

```powershell
cd frontend
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

## API Endpoints

### Health check

```text
GET /
```

### Process answer sheet

```text
POST /api/process-answer-sheet
```

Performs:

1. Image upload
2. OCR
3. Answer structuring
4. Parser confidence calculation

### Evaluate answers

```text
POST /api/evaluate
```

Performs rubric-based evaluation for each question and returns:

- suggested marks
- rubric breakdown
- evidence
- confidence
- missing concepts
- manual-review status
- total score
- percentage

## Grading Philosophy

The model is instructed to:

- follow the teacher's rubric
- evaluate every criterion separately
- avoid awarding marks for keywords alone
- accept equivalent wording when the intended concept is clear
- avoid inventing information
- avoid assuming omitted explanations
- flag uncertain cases for teacher review

The generated score is always a **suggested score**.

## Important Limitation

This project is a local prototype. The frontend currently communicates with a locally running Flask backend, and the backend communicates with a local Ollama/Qwen3 instance.

The system should not be treated as a replacement for a teacher's final assessment.

## Resume Description

**AI Answer Pre-Grader — Python, Flask, EasyOCR, Ollama, Qwen3**

Built an AI-assisted handwritten examination pre-grading system that uses OCR to extract student answers, Qwen3 to structure responses, and rubric-based evaluation to generate suggested marks, evidence, confidence scores, and manual-review flags while keeping the teacher in final control.

## Author

**Saanthosh M G**

GitHub: https://github.com/SAANTHOSH-M-G
