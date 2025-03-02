# recommendation/views.py

from django.shortcuts import render , redirect
from .recommend import get_recommendations

def recommendation_dashboard(request):
    if request.user.is_authenticated:
        recommendations = get_recommendations(request.user)

        return render(request, 'recommendations.html', {
            'recommendations': recommendations
        })
    else:
        return redirect('login')
