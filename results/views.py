import io
import csv
import json
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

    standard_list = ['5', '6', '7', '8', '9', '10']
    standard_toppers = []

    all_students = list(Student.objects.select_related('branch_group').prefetch_related('scores__subject').all())

    for std in standard_list:
        std_students = [s for s in all_students if str(s.standard).strip() == std and s.scores.exists()]
        if std_students:
            top_student = max(std_students, key=lambda s: s.percentage)
            standard_toppers.append({
                'standard': std,
                'student': top_student
            })
        else:
            standard_toppers.append({
                'standard': std,
                'student': None
            })

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
        "standard_toppers": standard_toppers,
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

            subject_alias_map = {
                'english': 'english',
                'इंग्रजी': 'english',
                'mathematics': 'mathematics',
                'गणित': 'mathematics',
                'science': 'science',
                'विज्ञान': 'science',
                'mathematics_1': 'mathematics_1',
                'mathematics 1': 'mathematics_1',
                'm1': 'mathematics_1',
                'गणित १': 'mathematics_1',
                'mathematics_2': 'mathematics_2',
                'mathematics 2': 'mathematics_2',
                'm2': 'mathematics_2',
                'गणित २': 'mathematics_2',
                'science_1': 'science_1',
                'science 1': 'science_1',
                's1': 'science_1',
                'विज्ञान १': 'science_1',
                'science_2': 'science_2',
                'science 2': 'science_2',
                's2': 'science_2',
                'विज्ञान २': 'science_2',
            }

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
                    clean_col = col.strip().lower()
                    canonical_key = subject_alias_map.get(clean_col)

                    if canonical_key and val and val.strip():
                        try:
                            marks = float(val.strip())
                            subj_obj, _ = Subject.objects.get_or_create(
                                code=canonical_key,
                                defaults={'name': canonical_key.replace('_', ' ').title()}
                            )
                            Score.objects.update_or_create(
                                student=student,
                                subject=subj_obj,
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
    header = [
        'roll_number', 'name', 'standard',
        'english', 'mathematics', 'science',
        'mathematics_1', 'mathematics_2', 'science_1', 'science_2'
    ]
    writer.writerow(header)
    writer.writerow(['101', 'राहुल शर्मा (५ वी)', '5', '35', '38', '36', '', '', '', ''])
    writer.writerow(['201', 'अनिकेत पाटील (९ वी)', '9', '72', '', '', '32', '35', '36', '38'])
    writer.writerow(['301', 'स्नेहल जोशी (१० वी)', '10', '75', '', '', '38', '39', '38', '37'])
    
    return response

@staff_member_required
def admin_analytics(request):
    students_qs = Student.objects.select_related('branch_group').prefetch_related('scores__subject').all()
    all_students = list(students_qs)
    sorted_all = sorted(all_students, key=lambda s: s.percentage, reverse=True)

    branches = BranchGroup.objects.all().order_by('name')
    standards = ['5', '6', '7', '8', '9', '10']

    # --- आलेख डेटा निर्मिती (Chart Data Calculation) ---
    chart_payload = {
        "branches": [b.name for b in branches],
        "standards": standards,
        "branch_standard_avg": {},  # Shakha -> Standard -> avg_percentage
        "branch_subject_avg": {},   # Shakha -> Standard -> Subject -> avg_marks
        "global_standard_avg": {},  # All Shakhas combined -> Standard -> avg_percentage
        "global_subject_avg": {},   # All Shakhas combined -> Standard -> Subject -> avg_marks
    }

    # प्राथमिक डेटा स्ट्रक्चर तयार करणे
    for b_name in chart_payload["branches"]:
        chart_payload["branch_standard_avg"][b_name] = {std: 0.0 for std in standards}
        chart_payload["branch_subject_avg"][b_name] = {std: {} for std in standards}

    for std in standards:
        chart_payload["global_standard_avg"][std] = 0.0
        chart_payload["global_subject_avg"][std] = {}

    # १. शाखानिहाय व इयत्तानिहाय विद्यार्थी गोळा करणे
    branch_std_students = {b_name: {std: [] for std in standards} for b_name in chart_payload["branches"]}
    global_std_students = {std: [] for std in standards}

    for s in all_students:
        std = str(s.standard).strip()
        b_name = s.branch_group.name if s.branch_group else None
        if std in standards:
            global_std_students[std].append(s)
            if b_name and b_name in branch_std_students:
                branch_std_students[b_name][std].append(s)

    # २. इयत्तानिहाय सरासरी टक्केवारी मोजणे (पाय चार्ट व तुलनात्मक आलेख)
    for std in standards:
        g_list = global_std_students[std]
        if g_list:
            chart_payload["global_standard_avg"][std] = round(sum(s.percentage for s in g_list) / len(g_list), 2)

        for b_name in chart_payload["branches"]:
            b_list = branch_std_students[b_name][std]
            if b_list:
                chart_payload["branch_standard_avg"][b_name][std] = round(sum(s.percentage for s in b_list) / len(b_list), 2)

    # ३. इयत्तानिहाय व विषयानुरूप सरासरी गुण मोजणे (बार आलेख २)
    subject_keys_std_5_8 = ['english', 'mathematics', 'science']
    subject_keys_std_9_10 = ['english', 'mathematics_1', 'mathematics_2', 'science_1', 'science_2']

    def calculate_subject_avg(students_list, std):
        target_keys = subject_keys_std_9_10 if std in ['9', '10'] else subject_keys_std_5_8
        subj_totals = {k: 0.0 for k in target_keys}
        subj_counts = {k: 0 for k in target_keys}

        for st in students_list:
            for sc in st.scores.all():
                code = (sc.subject.code or "").lower()
                name = sc.subject.name.lower()
                # alias मॅपिंग
                matched_key = None
                for tk in target_keys:
                    if tk in code or code in tk or tk in name or name in tk:
                        matched_key = tk
                        break
                if matched_key:
                    subj_totals[matched_key] += sc.marks_obtained
                    subj_counts[matched_key] += 1

        result = {}
        for k in target_keys:
            result[k] = round(subj_totals[k] / subj_counts[k], 2) if subj_counts[k] > 0 else 0.0
        return result

    for std in standards:
        chart_payload["global_subject_avg"][std] = calculate_subject_avg(global_std_students[std], std)
        for b_name in chart_payload["branches"]:
            chart_payload["branch_subject_avg"][b_name][std] = calculate_subject_avg(branch_std_students[b_name][std], std)

    context = {
        "students": sorted_all,
        "branches": branches,
        "standards": standards,
        "total_count": len(all_students),
        "chart_payload_json": json.dumps(chart_payload),
    }
    return render(request, "results/analytics.html", context)