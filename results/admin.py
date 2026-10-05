from django.contrib import admin
from .models import Student, Subject, Score

class ScoreInline(admin.TabularInline):
    model = Score
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_number', 'name', 'batch', 'get_percentage', 'get_status')
    search_fields = ('name', 'roll_number')
    list_filter = ('batch',)
    inlines = [ScoreInline]

    def get_percentage(self, obj):
        return f"{obj.percentage}%"
    get_percentage.short_description = "Percentage"

    def get_status(self, obj):
        return "Pass" if obj.is_passed else "Needs Improvement / Fail"
    get_status.short_description = "Status"

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_marks', 'passing_marks')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks_obtained', 'is_passed')
    list_filter = ('subject',)
    search_fields = ('student__name', 'student__roll_number')
