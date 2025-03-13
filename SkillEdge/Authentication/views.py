from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from Performance.models import Semester
from Recommendation.recommend import get_recommendations

def HomePage(request):
    return render(request, 'home.html')

@login_required
def DashBoard(request):
    # Fetch semesters and subjects data for the logged-in user
    semesters = Semester.objects.filter(user=request.user).prefetch_related('subjects')

    # Prepare semester performance data
    semester_data = []
    for semester in semesters:
        subjects = semester.subjects.all()
        total_marks = sum(sub.obtained_marks for sub in subjects if sub.obtained_marks is not None)
        max_marks = sum(sub.max_marks for sub in subjects)
        avg_marks = (total_marks / max_marks) * 100 if max_marks > 0 else 0

        semester_data.append({
            'semester_name': semester.name,
            'avg_marks': avg_marks,
            'subjects': [{'name': subj.name, 'marks': subj.obtained_marks, 'max_marks': subj.max_marks} for subj in subjects]
        })

    # Fetch AI recommendations for the user
    recommendations = get_recommendations(request.user)

    context = {
        'semester_data': semester_data,
        'recommendations': recommendations,
    }
    return render(request, 'dashboard.html', context)

def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            # Check if email exists, as `authenticate` uses username by default
            user = User.objects.get(email=email)
            username = user.username
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Dashboard')
            else:
                return render(request, 'login.html', {'error': 'Invalid email or password'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')

def Signup(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return render(request, 'signup.html', {'error': "Passwords don't match"})

        if User.objects.filter(username=uname).exists():
            return render(request, 'signup.html', {'error': "Username already exists. Please choose another one."})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': "Email already exists. Please use a different email address."})

        User.objects.create_user(uname, email, pass1)
        return redirect('Login')
    return render(request, 'signup.html')

@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def profile_edit_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'edit_profile.html', context)

@login_required
def create_roadmap(request):
    """View to generate a new roadmap using Gemini AI"""
    # Check if the user has interests and career goals in their profile
    user_profile = request.user.profile
    
    # Enhance the profile information with more context if needed
    interests = user_profile.interests
    if interests and len(interests.strip()) < 50:  # If too brief
        messages.warning(request, "Please provide more detailed interests in your profile (at least 50 characters).")
        return redirect('profile_edit')
    
    career_goals = user_profile.career_goals
    if career_goals and len(career_goals.strip()) < 50:  # If too brief
        messages.warning(request, "Please provide more detailed career goals in your profile (at least 50 characters).")
        return redirect('profile_edit')
    
    # Rest of the view code remains the same...