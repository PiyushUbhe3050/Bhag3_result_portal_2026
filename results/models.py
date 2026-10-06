from django.db import models
from django.contrib.auth.models import User

class BranchGroup(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name="शाखा नाव")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="पत्ता / ठिकाण")
    co_admin = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name="managed_branches",
        verbose_name="शाखा प्रमुख / Co-Admin"
    )

    class Meta:
        verbose_name = "शाखा गट"
        verbose_name_plural = "शाखा गट (Branches)"

    def __str__(self):
        return self.name

class Student(models.Model):
    branch_group = models.ForeignKey(
        BranchGroup, 
        on_delete=models.CASCADE, 
        related_name="students",
        null=True,
        blank=True,
        verbose_name="शाखा"
    )
    name = models.CharField(max_length=150, verbose_name="वर्धक नाव (Student Name)")
    roll_number = models.CharField(max_length=50, verbose_name="Roll Number")
    contact_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="संपर्क क्रमांक")

    class Meta:
        verbose_name = "विद्यार्थी / वर्धक"
        verbose_name_plural = "विद्यार्थी / वर्धक (Students)"
        unique_together = ('branch_group', 'roll_number')

    def __str__(self):
        branch = self.branch_group.name if self.branch_group else "No Branch"
        return f"{self.name} (Roll: {self.roll_number}) - {branch}"

    @property
    def total_marks_obtained(self):
        return sum(score.marks_obtained for score in self.scores.all())

    @property
    def total_max_marks(self):
        return sum(score.subject.max_marks for score in self.scores.all())

    @property
    def percentage(self):
        if self.total_max_marks > 0:
            return round((self.total_marks_obtained / self.total_max_marks) * 100, 2)
        return 0.0

    @property
    def overall_grade(self):
        pct = self.percentage
        if not self.is_passed:
            return "F"
        if pct >= 85:
            return "A+"
        elif pct >= 70:
            return "A"
        elif pct >= 60:
            return "B+"
        elif pct >= 50:
            return "B"
        elif pct >= 35:
            return "C"
        return "D"

    @property
    def is_passed(self):
        scores = self.scores.all()
        if not scores.exists():
            return False
        return all(score.is_passed for score in scores)

class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="विषयाचे नाव")
    max_marks = models.PositiveIntegerField(default=100, verbose_name="एकूण गुण (Max Marks)")
    passing_marks = models.PositiveIntegerField(default=35, verbose_name="उत्तीर्ण गुण (Passing Marks)")

    class Meta:
        verbose_name = "विषय"
        verbose_name_plural = "विषय (Subjects)"

    def __str__(self):
        return f"{self.name} (एकूण: {self.max_marks})"

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores", verbose_name="वर्धक")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="विषय")
    marks_obtained = models.FloatField(verbose_name="मिळालेले गुण")

    class Meta:
        verbose_name = "गुण नोंद"
        verbose_name_plural = "गुण नोंद (Scores)"
        unique_together = ('student', 'subject')

    @property
    def is_passed(self):
        return self.marks_obtained >= self.subject.passing_marks

    @property
    def grade(self):
        if not self.is_passed:
            return "F"
        pct = (self.marks_obtained / self.subject.max_marks) * 100 if self.subject.max_marks > 0 else 0
        if pct >= 85:
            return "A+"
        elif pct >= 70:
            return "A"
        elif pct >= 60:
            return "B+"
        elif pct >= 50:
            return "B"
        elif pct >= 35:
            return "C"
        return "D"

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks_obtained}"