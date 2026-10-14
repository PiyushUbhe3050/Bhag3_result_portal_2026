from django.db import models
from django.contrib.auth.models import User

# इयत्तेनुसार विषयांचे कमाल गुण व उत्तीर्ण गुणांचे अधिकृत निकष
STANDARD_SUBJECT_RULES = {
    '5': {
        'english': {'name': 'इंग्रजी (English)', 'max': 40, 'pass': 14},
        'mathematics': {'name': 'गणित (Mathematics)', 'max': 40, 'pass': 14},
        'science': {'name': 'विज्ञान (Science)', 'max': 40, 'pass': 14},
    },
    '6': {
        'english': {'name': 'इंग्रजी (English)', 'max': 40, 'pass': 14},
        'mathematics': {'name': 'गणित (Mathematics)', 'max': 40, 'pass': 14},
        'science': {'name': 'विज्ञान (Science)', 'max': 40, 'pass': 14},
    },
    '7': {
        'english': {'name': 'इंग्रजी (English)', 'max': 50, 'pass': 18},
        'mathematics': {'name': 'गणित (Mathematics)', 'max': 40, 'pass': 14},
        'science': {'name': 'विज्ञान (Science)', 'max': 50, 'pass': 18},
    },
    '8': {
        'english': {'name': 'इंग्रजी (English)', 'max': 50, 'pass': 18},
        'mathematics': {'name': 'गणित (Mathematics)', 'max': 44, 'pass': 16},
        'science': {'name': 'विज्ञान (Science)', 'max': 50, 'pass': 18},
    },
    '9': {
        'english': {'name': 'इंग्रजी (English)', 'max': 80, 'pass': 28},
        'mathematics_1': {'name': 'गणित भाग १ (Mathematics 1)', 'max': 36, 'pass': 13},
        'mathematics_2': {'name': 'गणित भाग २ (Mathematics 2)', 'max': 40, 'pass': 14},
        'science_1': {'name': 'विज्ञान भाग १ (Science 1)', 'max': 40, 'pass': 14},
        'science_2': {'name': 'विज्ञान भाग २ (Science 2)', 'max': 40, 'pass': 14},
    },
    '10': {
        'english': {'name': 'इंग्रजी (English)', 'max': 80, 'pass': 28},
        'mathematics_1': {'name': 'गणित भाग १ (Mathematics 1)', 'max': 40, 'pass': 14},
        'mathematics_2': {'name': 'गणित भाग २ (Mathematics 2)', 'max': 40, 'pass': 14},
        'science_1': {'name': 'विज्ञान भाग १ (Science 1)', 'max': 40, 'pass': 14},
        'science_2': {'name': 'विज्ञान भाग २ (Science 2)', 'max': 40, 'pass': 14},
    },
}

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
    STANDARD_CHOICES = [
        ('5', '५ वी (5th Standard)'),
        ('6', '६ वी (6th Standard)'),
        ('7', '७ वी (7th Standard)'),
        ('8', '८ वी (8th Standard)'),
        ('9', '९ वी (9th Standard)'),
        ('10', '१० वी (10th Standard)'),
    ]

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
    standard = models.CharField(
        max_length=10, 
        choices=STANDARD_CHOICES, 
        default='5', 
        verbose_name="इयत्ता (Standard)"
    )
    contact_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="संपर्क क्रमांक")

    class Meta:
        verbose_name = "विद्यार्थी / वर्धक"
        verbose_name_plural = "विद्यार्थी / वर्धक (Students)"
        unique_together = ('branch_group', 'roll_number')

    def __str__(self):
        branch = self.branch_group.name if self.branch_group else "No Branch"
        return f"{self.name} (इ. {self.standard} वी | Roll: {self.roll_number}) - {branch}"

    def get_subject_specs(self):
        std = str(self.standard).strip()
        return STANDARD_SUBJECT_RULES.get(std, STANDARD_SUBJECT_RULES['5'])

    @property
    def total_marks_obtained(self):
        return round(sum(score.marks_obtained for score in self.scores.all()), 2)

    @property
    def total_max_marks(self):
        specs = self.get_subject_specs()
        return sum(details['max'] for details in specs.values())

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

class Subject(models.Model):
    # unique=True काढले आहे व blank=True, null=True ठेवले आहे जेणेकरून मायग्रेशन अडकणार नाही
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="विषय कोड (Key)")
    name = models.CharField(max_length=100, verbose_name="विषयाचे नाव")
    max_marks = models.PositiveIntegerField(default=100, verbose_name="डीफॉल्ट कमाल गुण")
    passing_marks = models.PositiveIntegerField(default=35, verbose_name="डीफॉल्ट उत्तीर्ण गुण")

    class Meta:
        verbose_name = "विषय"
        verbose_name_plural = "विषय (Subjects)"

    def __str__(self):
        return f"{self.name}"

class Score(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="scores", verbose_name="वर्धक")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="विषय")
    marks_obtained = models.FloatField(verbose_name="मिळालेले गुण")

    class Meta:
        verbose_name = "गुण नोंद"
        verbose_name_plural = "गुण नोंद (Scores)"
        unique_together = ('student', 'subject')

    def get_actual_spec(self):
        specs = self.student.get_subject_specs()
        code = (self.subject.code or "").lower()
        name = self.subject.name.lower()

        if code in specs:
            return specs[code]
        for k, v in specs.items():
            if k in code or code in k or k in name or name in k:
                return v
        return {'max': self.subject.max_marks, 'pass': self.subject.passing_marks, 'name': self.subject.name}

    @property
    def actual_max_marks(self):
        return self.get_actual_spec()['max']

    @property
    def actual_passing_marks(self):
        return self.get_actual_spec()['pass']

    @property
    def display_subject_name(self):
        return self.get_actual_spec()['name']

    @property
    def is_passed(self):
        return self.marks_obtained >= self.actual_passing_marks

    @property
    def grade(self):
        if not self.is_passed:
            return "F"
        max_m = self.actual_max_marks
        pct = (self.marks_obtained / max_m) * 100 if max_m > 0 else 0
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
        return f"{self.student.name} - {self.display_subject_name}: {self.marks_obtained}"