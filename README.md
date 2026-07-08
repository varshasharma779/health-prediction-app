# Health Prediction App

An AI-powered web application that predicts possible health conditions 
based on patient blood test results.

## Tech Stack
- **Backend:** Python + Flask
- **Frontend:** HTML + CSS + Bootstrap
- **Database:** SQLite
- **AI:** Groq API (Llama 3.3 70B)

## Features
- Add, View, Edit, Delete patient records (CRUD)
- Blood test input: Glucose, Haemoglobin, Cholesterol
- AI automatically generates health prediction remarks
- Input validation on all fields
- Persistent SQLite storage

## Setup Instructions

### 1. Clone the repository
git clone https://github.com/varshasharma779/health-prediction-app.git
cd health-prediction-app

### 2. Install dependencies
pip install -r requirements.txt

### 3. Add your API key
- Get a FREE Groq API key at: https://console.groq.com
- Create a file named .env in the project root
- Add this line to your .env file:

GROQ_API_KEY=your-groq-api-key-here

### 4. Run the application
python app.py

### 5. Open in browser
http://localhost:5000

## Project Structure
health-prediction-app/
├── app.py               # Flask backend + Groq AI integration
├── database.py          # SQLite CRUD operations
├── requirements.txt     # Python dependencies
├── .env.example         # API key template
├── templates/
│   └── index.html       # Frontend HTML
└── static/
    └── style.css        # Stylesheet