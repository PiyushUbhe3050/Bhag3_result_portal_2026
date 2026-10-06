import io
import csv
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Avg
from .models import BranchGroup, Student, Subject, Score

def search_result(request):
    branches = BranchGroup.objects.all().order_by('name')
    error = None

    if request.method == "POST":
        branch_id = request.POST.get("branch_group", "").strip()
        roll_number = request.POST.get("roll_number", "").strip()
        name = request.POST.get("name", "").strip()

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
    """
    Allows Super-Admin and Branch Co-Admins to upload CSV / XLSX files.
    """
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

        # Verify permission on branch
        if not request.user.is_superuser:
            target_branch = BranchGroup.objects.filter(id=branch_id, co_admin=request.user).first()
        else:
            target_branch = BranchGroup.objects.filter(id=branch_id).first()

        if not target_branch:
            messages.error(request, "तुम्हाला या शाखेमध्ये माहिती भरण्याची परवानगी नाही.")
            return redirect('bulk_upload')

        # Read CSV or Excel
        try:
            file_name = uploaded_file.name.lower()
            if file_name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, dtype={'roll_number': str})
            elif file_name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file, dtype={'roll_number': str})
            else:
                messages.error(request, "केवळ .xlsx किंवा .csv फॉरमॅट मधील फाईल अपलोड करा.")
                return redirect('bulk_upload')

            # Clean headers
            df.columns = [str(c).strip().lower() for c in df.columns]

            if 'roll_number' not in df.columns or 'name' not in df.columns:
                messages.error(request, "फाईलमध्ये 'roll_number' आणि 'name' हे दोन मुख्य कॉलम असणे आवश्यक आहे.")
                return redirect('bulk_upload')

            # Map available subjects in DB
            db_subjects = {s.name.strip().lower(): s for s in Subject.objects.all()}

            records_created = 0
            records_updated = 0

            for _, row in df.iterrows():
                roll_no = str(row['roll_number']).strip()
                student_name = str(row['name']).strip()
                if not roll_no or not student_name or roll_no.lower() == 'nan':
                    continue

                student, created = Student.objects.update_or_create(
                    branch_group=target_branch,
                    roll_number=roll_no,
                    defaults={'name': student_name}
                )

                if created:
                    records_created += 1
                else:
                    records_updated += 1

                # Process subject marks for remaining columns
                for col in df.columns:
                    if col in ['roll_number', 'name', 'contact_number']:
                        continue
                    if col in db_subjects:
                        raw_marks = row[col]
                        try:
                            if pd.notna(raw_marks):
                                marks = float(raw_marks)
                                Score.objects.update_or_create(
                                    student=student,
                                    subject=db_subjects[col],
                                    defaults={'marks_obtained': marks}
                                )
                        except (ValueError, TypeError):
                            pass

            messages.success(request, f"यशस्वी! {records_created} नवीन विद्यार्थी जोडले गेले व {records_updated} विद्यार्थ्यांचे गुण अपडेट झाले.")
            return redirect('admin:results_student_changelist')

        except Exception as e:
            messages.error(request, f"फाईल प्रोसेस करताना त्रुटी आली: {str(e)}")
            return redirect('bulk_upload')

    return render(request, "admin/bulk_upload.html", {
        "branches": branches,
        "subjects": Subject.objects.all()
    })

@staff_member_required
def download_sample_csv(request):
    """
    Downloads a ready-to-use CSV template matching subjects in DB.
    """
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="student_marks_template.csv"'
    
    # Write UTF-8 BOM so Excel opens Marathi characters properly
    response.write('\ufeff'.encode('utf8'))
    
    writer = csv.writer(response)
    subjects = [s.name for s in Subject.objects.all()]
    header = ['roll_number', 'name'] + subjects
    writer.writerow(header)
    
    # Example dummy row
    sample_row = ['101', 'राहुल सुरेश शर्मा'] + ['35' for _ in subjects]
    writer.writerow(sample_row)
    
    return response

@staff_member_required
def admin_analytics(request):
    students = Student.objects.prefetch_related('scores__subject', 'branch_group').all()
    if not request.user.is_superuser:
        students = students.filter(branch_group__co_admin=request.user)

    students = list(students)
    total_students = len(students)
    passed_students = [s for s in students if s.is_passed]
    pass_percentage = round((len(passed_students) / total_students * 100), 2) if total_students > 0 else 0

    avg_score = Score.objects.filter(
        student__in=students
    ).aggregate(avg=Avg('marks_obtained'))['avg'] or 0

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