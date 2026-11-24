import joblib
import pandas as pd

# Load trained models
gpa_model = joblib.load("models/gpa_model.pkl")
performance_model = joblib.load("models/performance_model.pkl")

# Feature order
FEATURES = [
    "Study_Hours_Per_Day",
    "Extracurricular_Hours_Per_Day",
    "Sleep_Hours_Per_Day",
    "Social_Hours_Per_Day",
    "Physical_Activity_Hours_Per_Day",
    "Stress_Score",
    "Attendance_Percentage"
]

def predict_student_performance(
    study_hours,
    extracurricular_hours,
    sleep_hours,
    social_hours,
    physical_activity,
    stress_score,
    attendance
):
    student_data = pd.DataFrame([[
        study_hours,
        extracurricular_hours,
        sleep_hours,
        social_hours,
        physical_activity,
        stress_score,
        attendance
    ]], columns=FEATURES)

    predicted_gpa = gpa_model.predict(student_data)[0]

    predicted_level = performance_model.predict(student_data)[0]

    return {
        "predicted_gpa": round(float(predicted_gpa), 2),
        "performance_level": str(predicted_level)
    }