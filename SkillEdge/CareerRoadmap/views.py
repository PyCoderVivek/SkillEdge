from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Roadmap, RoadmapMilestone, Resource
from .gemini_utils import generate_career_roadmap
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

@login_required
def roadmap_dashboard(request):
    """View to display the user's roadmaps and option to create new ones"""
    roadmaps = Roadmap.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'roadmap_dashboard.html', {'roadmaps': roadmaps})

@login_required
def create_roadmap(request):
    """View to generate a new roadmap using Gemini AI"""
    # Check if the user has interests and career goals in their profile
    user_profile = request.user.profile
    interests = user_profile.interests
    career_goals = user_profile.career_goals
    
    if not interests or not career_goals:
        messages.warning(request, "Please update your interests and career goals in your profile first.")
        return redirect('profile_edit')
    
    if request.method == 'POST':
        # Generate roadmap using Gemini
        roadmap_data = generate_career_roadmap(interests, career_goals)
        
        # Save the roadmap to the database
        roadmap = Roadmap.objects.create(
            user=request.user,
            title=roadmap_data.get('title', 'Your Career Roadmap'),
            description=roadmap_data.get('description', '')
        )
        
        # Create milestones for the roadmap
        for i, milestone_data in enumerate(roadmap_data.get('milestones', [])):
            milestone = RoadmapMilestone.objects.create(
                roadmap=roadmap,
                title=milestone_data.get('title', f'Milestone {i+1}'),
                description=milestone_data.get('description', ''),
                time_frame=milestone_data.get('time_frame', ''),
                order=i
            )
            
            # Create resources for each milestone
            for resource_data in milestone_data.get('resources', []):
                Resource.objects.create(
                    milestone=milestone,
                    title=resource_data.get('title', ''),
                    url=resource_data.get('url', ''),
                    description=resource_data.get('description', ''),
                    resource_type=resource_data.get('resource_type', '')
                )
        
        messages.success(request, "Your career roadmap has been generated successfully!")
        return redirect('view_roadmap', roadmap_id=roadmap.id)
    
    return render(request, 'create_roadmap.html', {
        'interests': interests,
        'career_goals': career_goals
    })

@login_required
def view_roadmap(request, roadmap_id):
    """View to display a specific roadmap with its milestones"""
    roadmap = Roadmap.objects.get(id=roadmap_id, user=request.user)
    milestones = roadmap.milestones.all().order_by('order')
    
    return render(request, 'view_roadmap.html', {
        'roadmap': roadmap,
        'milestones': milestones
    })

@login_required
def delete_roadmap(request, roadmap_id):
    """View to delete a roadmap"""
    if request.method == 'POST':
        roadmap = Roadmap.objects.get(id=roadmap_id, user=request.user)
        roadmap.delete()
        messages.success(request, "Roadmap deleted successfully.")
        return redirect('roadmap_dashboard')
    
    return redirect('roadmap_dashboard')

@staff_member_required
def test_roadmap_generation(request):
    """Admin-only view to test the roadmap generation"""
    test_interests = """
    I'm passionate about full-stack web development with React and Node.js. 
    I enjoy working with databases (particularly MongoDB and PostgreSQL), 
    and I'm interested in cloud technologies like AWS and serverless architecture. 
    I've recently started exploring machine learning and data visualization.
    """
    
    test_career_goals = """
    I aim to become a senior full-stack developer within 2 years. 
    Long-term, I want to transition into a technical leadership role where I can 
    architect solutions and mentor junior developers. I'm particularly interested 
    in fintech and healthcare sectors. Eventually, I'd like to start my own tech consultancy.
    """
    
    try:
        roadmap_data = generate_career_roadmap(test_interests, test_career_goals)
        return JsonResponse({
            'success': True,
            'roadmap': roadmap_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })
