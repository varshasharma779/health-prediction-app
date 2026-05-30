from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from database import init_db, create_patient, get_all_patients, get_patient_by_id, update_patient, delete_patient
from groq import Groq
from dotenv import load_dotenv
import re
from datetime import datetime, date
import os
load_dotenv()
app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
init_db()

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None

def validate_dob(dob_str):
    try:
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
        return dob < date.today()
    except ValueError:
        return False

def validate_numeric(value):
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False

def validate_patient_data(data):
    errors = []
    if not data.get("full_name", "").strip():
        errors.append("Full name is required.")
    if not validate_dob(data.get("dob", "")):
        errors.append("Date of birth must be a valid past date (YYYY-MM-DD).")
    if not validate_email(data.get("email", "")):
        errors.append("Invalid email address format.")
    for field in ["glucose", "haemoglobin", "cholesterol"]:
        if not validate_numeric(data.get(field)):
            errors.append(f"{field.capitalize()} must be a numeric value.")
    return errors

#AI prediction

def get_ai_prediction(full_name, glucose, haemoglobin, cholesterol):
    prompt = f"""

    You are a medical AI assistant. Based on the following blood test results for a patient,
    provide a brief health risk assessment and possible health conditions.
    Be concise (2-3 sentences), mention any risks, and recommend consulting a doctor.

    Patient: {full_name}
    - Blood Glucose: {glucose} mg/dL  (Normal: 70-100 mg/dL fasting)
    - Haemoglobin: {haemoglobin} g/dL  (Normal: Men 13.5-17.5, Women 12-15.5)
    - Cholesterol: {cholesterol} mg/dL  (Normal: below 200 mg/dL)

    Provide a health prediction remark in 2-3 sentences:
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful medical AI assistant that analyzes blood test results and provides brief health risk assessments."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=200,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"AI prediction unavailable: {str(e)}"




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/patients", methods=["GET"])
def api_get_patients():
    patients = get_all_patients()
    return jsonify(patients)

@app.route("/api/patients/<int:patient_id>", methods=["GET"])
def api_get_patient(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify(patient)

@app.route("/api/patients", methods=["POST"])
def api_create_patient():
    data = request.get_json()
    errors = validate_patient_data(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    remarks = get_ai_prediction(
        data["full_name"],
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"])
    )

    result = create_patient(
        data["full_name"].strip(),
        data["dob"],
        data["email"].strip(),
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"]),
        remarks
    )

    if result["success"]:
        patient = get_patient_by_id(result["id"])
        return jsonify({"success": True, "patient": patient}), 201
    return jsonify({"success": False, "errors": [result["error"]]}), 400

@app.route("/api/patients/<int:patient_id>", methods=["PUT"])
def api_update_patient(patient_id):
    data = request.get_json()
    errors = validate_patient_data(data)
    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    remarks = get_ai_prediction(
        data["full_name"],
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"])
    )

    result = update_patient(
        patient_id,
        data["full_name"].strip(),
        data["dob"],
        data["email"].strip(),
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"]),
        remarks
    )

    if result["success"]:
        patient = get_patient_by_id(patient_id)
        return jsonify({"success": True, "patient": patient})
    return jsonify({"success": False, "errors": [result["error"]]}), 400

@app.route("/api/patients/<int:patient_id>", methods=["DELETE"])
def api_delete_patient(patient_id):
    patient = get_patient_by_id(patient_id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    result = delete_patient(patient_id)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)