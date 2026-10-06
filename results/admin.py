from django.contrib import admin
from .models import BranchGroup, Student, Subject, Score

class ScoreInline(admin.TabularInline):
    model = Score
    extra = 1

@admin.register(BranchGroup)
class BranchGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'co_admin')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(co_admin=request.user)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'branch_group', 'get_percentage', 'get_status')
    search_fields = ('name', 'roll_number')
    list_filter = ('branch_group',)
    inlines = [ScoreInline]

    def get_percentage(self, obj):
        return f"{obj.percentage}%"
    get_percentage.short_description = "टक्केवारी (Percentage)"

    def get_status(self, obj):
        return "उत्तीर्ण (Pass)" if obj.is_passed else "मार्गदर्शन आवश्यक (Needs Help)"
    get_status.short_description = "निकाल (Status)"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(branch_group__co_admin=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "branch_group" and not request.user.is_superuser:
            kwargs["queryset"] = BranchGroup.objects.filter(co_admin=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_marks', 'passing_marks')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks_obtained', 'is_passed')
    list_filter = ('subject', 'student__branch_group')
    search_fields = ('student__name', 'student__roll_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(student__branch_group__co_admin=request.user)