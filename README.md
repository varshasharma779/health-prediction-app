# Health Prediction App

AI-powered patient health prediction using blood test results.

## Tech Stack
- Backend: Python + Flask
- Frontend: HTML + Bootstrap
- Database: SQLite
- AI: Groq API (Llama 3.3 70B)

## Setup Instructions

### 1. Clone the repo
git clone https://github.com/varshasharma779/health-prediction-app.git
cd health-prediction-app

### 2. Install dependencies
pip install -r requirements.txt

### 3. Create .env file
Create a file named `.env` and add:
GROQ_API_KEY=your-groq-api-key
Get your key at: https://console.groq.com

### 4. Run the app
python app.py

### 5. Open in browser
http://localhost:5000

## Features
- Add, View, Edit, Delete patient records (CRUD)
- Blood test input: Glucose, Haemoglobin, Cholesterol
- AI automatically generates health prediction remarks
- Data validation on all fields
- SQLite persistent storage