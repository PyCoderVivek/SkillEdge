import numpy as np
from sklearn.linear_model import LinearRegression
from .models import Semester, Subject

def predict_next_semester_avg(user):
    # Fetch semesters and their subjects for the logged-in user
    semesters = Semester.objects.filter(user=user).prefetch_related('subjects')

    # Prepare data for prediction
    X = []  # Semester indices (1, 2, 3,...)
    y = []  # Average marks per semester

    for idx, semester in enumerate(semesters, start=1):
        subjects = semester.subjects.all()
        total_marks = sum(subject.obtained_marks for subject in subjects if subject.obtained_marks is not None)
        max_marks = sum(subject.max_marks for subject in subjects)
        
        if max_marks > 0:
            avg_marks = (total_marks / max_marks) * 100
            X.append([idx])  # Using 2D array for sklearn
            y.append(avg_marks)
    
    if len(X) < 2:
        # Not enough data to predict
        return None

    # Train the prediction model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the next semester's average
    next_semester_index = len(X) + 1
    predicted_avg = model.predict([[next_semester_index]])

    return max(0, min(predicted_avg[0], 100))  # Ensuring the prediction is within 0-100
