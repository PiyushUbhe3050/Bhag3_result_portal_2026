from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg
from .models import Student, Score, Subject

def search_result(request):
    error = None
    student = None
    scores = []

    if request.method == "POST":
        roll_number = request.POST.get("roll_number", "").strip()
        name = request.POST.get("name", "").strip()

        try:
            student = Student.objects.get(roll_number__iexact=roll_number, name__icontains=name)
            scores = student.scores.select_related('subject').all()
        except Student.DoesNotExist:
            error = "No student found matching that Roll Number and Name combination."

    return render(request, "results/search.html", {
        "student": student,
        "scores": scores,
        "error": error
    })

@staff_member_required
def admin_analytics(request):
    students = list(Student.objects.prefetch_related('scores__subject').all())
    
    total_students = len(students)
    passed_students = [s for s in students if s.is_passed]
    pass_percentage = round((len(passed_students) / total_students * 100), 2) if total_students > 0 else 0
    
    avg_score = Score.objects.aggregate(avg=Avg('marks_obtained'))['avg'] or 0

    sorted_students = sorted(students, key=lambda s: s.percentage, reverse=True)
    toppers = sorted_students[:5]
    at_risk = [s for s in sorted_students if not s.is_passed or s.percentage < 40]

    return render(request, "results/analytics.html", {
        "total_students": total_students,
        "pass_percentage": pass_percentage,
        "avg_score": round(avg_score, 2),
        "toppers": toppers,
        "at_risk": at_risk,
    })
