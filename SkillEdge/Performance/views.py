from django.shortcuts import render, redirect , get_object_or_404
from .models import Semester , Subject
from .forms import SemesterForm, SubjectForm
from .prediction_model import predict_next_semester_avg

def manage_performance(request):
    semesters = Semester.objects.filter(user=request.user)
    semester_form = SemesterForm()
    subject_form = SubjectForm()

    if request.method == "POST":
        if 'add_semester' in request.POST:
            semester_form = SemesterForm(request.POST)
            if semester_form.is_valid():
                semester = semester_form.save(commit=False)
                semester.user = request.user
                semester.save()
                return redirect('manage_performance')

        elif 'add_subject' in request.POST:
            subject_form = SubjectForm(request.POST)
            if subject_form.is_valid():
                subject = subject_form.save(commit=False)
                subject.semester_id = request.POST.get('semester_id')  # Assign semester ID dynamically
                subject.save()
                return redirect('manage_performance')

    return render(request, 'performance/add_performance_data.html', {
        'semesters': semesters,
        'semester_form': semester_form,
        'subject_form': subject_form,
    })

def performance_dashboard(request):
    semesters = Semester.objects.filter(user=request.user).prefetch_related('subjects')

    semester_data = []
    for semester in semesters:
        subjects = semester.subjects.all()
        total_marks = sum(subject.obtained_marks for subject in subjects if subject.obtained_marks is not None)
        max_marks = sum(subject.max_marks for subject in subjects)
        avg_marks = (total_marks / max_marks) * 100 if max_marks > 0 else 0

        semester_data.append({
            'semester_name': semester.name,
            'avg_marks': avg_marks,
            'subjects': [{'name': subj.name, 'marks': subj.obtained_marks, 'max_marks': subj.max_marks} for subj in subjects]
        })

    # Predict the next semester's average
    predicted_avg = predict_next_semester_avg(request.user)

    context = {
        'semester_data': semester_data,
        'predicted_avg': predicted_avg,
    }

    return render(request, 'performance/performance.html', context)


def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == "POST":
        subject.delete()
        return redirect('manage_performance')
    
    return render(request, 'add_performance_data.html', {'subject': subject})
