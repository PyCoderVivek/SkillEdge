from django import forms
from .models import Semester, Subject

class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['name']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'max_marks', 'obtained_marks']
