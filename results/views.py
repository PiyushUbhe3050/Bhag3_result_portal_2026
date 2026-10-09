import io
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse
from .models import BranchGroup, Student, Subject, Score

@csrf_exempt
def search_result(request):
    branches = BranchGroup.objects.all().order_by('name')
    error = None

    branch_id = request.GET.get("branch_group", "").strip() or request.POST.get("branch_group", "").strip()
    roll_number = request.GET.get("roll_number", "").strip() or request.POST.get("roll_number", "").strip()
    name = request.GET.get("name", "").strip() or request.POST.get("name", "").strip()

    if branch_id and roll_number and name:
        try:
            student = Student.objects.get(
                branch_group_id=branch_id,
                roll_number__iexact=roll_number,
                name__icontains=name
            )
            return redirect(f'/result/{student.id}/')
        except Student.DoesNotExist:
            error = "दिलेल्या शाखा, Roll Number आणि नावाची कोणतीही नोंद आढळली नाही. कृपया योग्य माहिती तपासा."

    return render(request, "results/search.html", {
        "branches": branches,
        "error": error
    })

def view_report_card(request, student_id):
    student = get_object_or_404(Student.objects.select_related('branch_group'), id=student_id)
    scores = student.scores.select_related('subject').all()
    
    return render(request, "results/report_card.html", {
        "student": student,
        "scores": scores,
        "is_passed": student.is_passed,
        "percentage": student.percentage,
    })

@staff_member_required
def bulk_upload_students(request):
    if request.user.is_superuser:
        branches = BranchGroup.objects.all().order_by('name')
    else:
        branches = BranchGroup.objects.filter(co_admin=request.user)

    if request.method == "POST":
        branch_id = request.POST.get("branch_group")
        uploaded_file = request.FILES.get("file")

        if not branch_id or not uploaded_file:
            messages.error(request, "कृपया शाखा निवडा आणि फाईल अपलोड करा.")
            return redirect('bulk_upload')

        if not request.user.is_superuser:
            target_branch = BranchGroup.objects.filter(id=branch_id, co_admin=request.user).first()
        else:
            target_branch = BranchGroup.objects.filter(id=branch_id).first()

        if not target_branch:
            messages.error(request, "तुम्हाला या शाखेमध्ये माहिती भरण्याची परवानगी नाही.")
            return redirect('bulk_upload')

        if not uploaded_file.name.lower().endswith('.csv'):
            messages.error(request, "कृपया केवळ .csv फाईल अपलोड करा.")
            return redirect('bulk_upload')

        try:
            file_data = uploaded_file.read().decode('utf-8-sig')
            reader = csv.DictReader(io.StringIO(file_data))

            fieldnames = [f.strip().lower() for f in reader.fieldnames if f]
            reader.fieldnames = fieldnames

            if 'roll_number' not in fieldnames or 'name' not in fieldnames:
                messages.error(request, "CSV फाईलमध्ये 'roll_number' आणि 'name' हे दोन मुख्य कॉलम असणे आवश्यक आहे.")
                return redirect('bulk_upload')

            db_subjects = {s.name.strip().lower(): s for s in Subject.objects.all()}

            records_created = 0
            records_updated = 0

            for row in reader:
                roll_no = str(row.get('roll_number', '')).strip()
                student_name = str(row.get('name', '')).strip()
                std = str(row.get('standard', '5')).strip()

                if not roll_no or not student_name:
                    continue

                student, created = Student.objects.update_or_create(
                    branch_group=target_branch,
                    roll_number=roll_no,
                    defaults={'name': student_name, 'standard': std}
                )

                if created:
                    records_created += 1
                else:
                    records_updated += 1

                for col, val in row.items():
                    if col in ['roll_number', 'name', 'standard', 'contact_number']:
                        continue
                    if col in db_subjects and val and val.strip():
                        try:
                            marks = float(val.strip())
                            Score.objects.update_or_create(
                                student=student,
                                subject=db_subjects[col],
                                defaults={'marks_obtained': marks}
                            )
                        except ValueError:
                            pass

            messages.success(request, f"यशस्वी! {records_created} नवीन विद्यार्थी जोडले गेले व {records_updated} विद्यार्थ्यांचे गुण अपडेट झाले.")
            return redirect('admin:results_student_changelist')

        except Exception as e:
            messages.error(request, f"CSV फाईल वाचताना त्रुटी आली: {str(e)}")
            return redirect('bulk_upload')

    return render(request, "admin/bulk_upload.html", {
        "branches": branches,
        "subjects": Subject.objects.all()
    })

@staff_member_required
def download_sample_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="student_marks_template.csv"'
    response.write('\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    subjects = [s.name for s in Subject.objects.all()]
    header = ['roll_number', 'name', 'standard'] + subjects
    writer.writerow(header)
    
    sample_row = ['101', 'राहुल सुरेश शर्मा', '5'] + ['35' for _ in subjects]
    writer.writerow(sample_row)
    
    return response

@staff_member_required
def admin_analytics(request):
    """
    Mobile-First Analytics:
    All Co-Admins and Super-Admins have full visibility across all branches and standards.
    """
    students_qs = Student.objects.select_related('branch_group').prefetch_related('scores__subject').all()
    all_students = list(students_qs)
    
    # Sort descending by percentage
    sorted_all = sorted(all_students, key=lambda s: s.percentage, reverse=True)
    top_5_students = sorted_all[:5]

    branches = BranchGroup.objects.all().order_by('name')
    standards = ['5', '6', '7', '8', '9', '10']

    context = {
        "top_5": top_5_students,
        "students": sorted_all,
        "branches": branches,
        "standards": standards,
        "total_count": len(all_students),
    }
    return render(request, "results/analytics.html", context)