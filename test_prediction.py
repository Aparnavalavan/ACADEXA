from prediction import predict_student_performance

result = predict_student_performance(
    study_hours=5,
    extracurricular_hours=2,
    sleep_hours=8,
    social_hours=3,
    physical_activity=2,
    stress_score=4,
    attendance=90
)

print("ACADEXA PREDICTION")
print("Estimated GPA:", result["predicted_gpa"])
print("Performance Level:", result["performance_level"])