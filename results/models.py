from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=150)
    roll_number = models.CharField(max_length=50, unique=True)
    batch = models.CharField(max_length=100, default="2026 NGO Batch")
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

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
    def is_passed(self):
        scores = self.scores.all()
        if not scores.exists():
            return False
        return all(score.is_passed for score in scores)

class Subject(models.Model):
    name = models.CharField(max_length=100)
    max_marks = models.PositiveIntegerField(default=100)
    passing_marks = models.PositiveIntegerField(default=35)

    def __str__(self):
        return f"{self.name} (Max: {self.max_marks})"

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.FloatField()

    class Meta:
        unique_together = ('student', 'subject')

    @property
    def is_passed(self):
        return self.marks_obtained >= self.subject.passing_marks

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.marks_obtained}"
