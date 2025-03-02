# recommendation/recommend.py

from Performance.models import Subject
from django.db.models import Avg

def get_recommendations(user):
    """
    A simple recommendation function to suggest subjects based on performance.
    This checks the user’s average performance and suggests subjects where
    they scored below average.
    """

    # Get all subjects for the user
    subjects = Subject.objects.filter(semester__user=user)

    # Calculate the average marks across all subjects for the user
    avg_marks = subjects.aggregate(Avg('obtained_marks'))['obtained_marks__avg']

    recommendations = []
    
    for subject in subjects:
        if subject.obtained_marks < avg_marks:
            recommendations.append({
                'subject_name': subject.name,
                'marks': subject.obtained_marks,
                'max_marks': subject.max_marks,
                'suggestion': f"Focus more on {subject.name}, you scored below average."
            })
    
    return recommendations
