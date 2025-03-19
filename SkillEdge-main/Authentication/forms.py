from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location', 'interests', 'career_goals']
        widgets = {
            'interests': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your interests...'}),
            'career_goals': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Your career goals...'}),
        }
