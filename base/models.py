import datetime
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser


# Create your models here.
class ModelManager(models.Manager):
    pass


class BaseModel(models.Model):
    objects = ModelManager()

    class Meta:
        abstract = True


class MentalUser(AbstractUser):
    ROLE_CHOICES = (
        ('Student', 'Student'),
        ('Consultant', 'Consultant'),
    )

    username = models.CharField(max_length=50, null=True)
    email = models.EmailField(unique=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def is_student(self):
        return self.role == 'Student'

    def is_consultant(self):
        return self.role == 'Consultant'

    class Meta:
        verbose_name = 'Mental User'


class Student(MentalUser):
    def save(self, *args, **kwargs):
        self.role = 'Student'
        super(Student, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Student'

    def __str__(self):
        return self.email


class Consultant(MentalUser):
    major = models.CharField(max_length=200)
    profilePicture = models.ImageField(null=True, blank=True, default='user.png', upload_to='profilePicture/')
    resume = models.FileField(null=True, blank=True, upload_to='resumes/')
    startTime = models.TimeField(default=datetime.time(9, 0), null=True, blank=True)
    endTime = models.TimeField(default=datetime.time(15, 10), null=True, blank=True)

    def save(self, *args, **kwargs):
        self.role = 'Consultant'
        super(Consultant, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Consultant'

    def __str__(self):
        return self.email


class DisordersContent(BaseModel, models.Model):
    Category = models.CharField(null=True, max_length=100)
    NavbarName = models.CharField(default='none', max_length=150)
    Title = models.CharField(max_length=150)
    definition = RichTextField()
    signs = RichTextField()
    advices = RichTextField()

    def __str__(self):
        return self.Title


class Session(BaseModel, models.Model):
    sessionDate = models.DateField(null=True)
    sessionTime = models.TimeField(null=True)
    sessionEndTime = models.DateTimeField(null=True)
    consultant = models.ForeignKey(Consultant, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"Std: {self.student.username} | Cons: {self.consultant.username} | Date: {self.sessionDate} | Time: {self.sessionTime}"


class Message(BaseModel, models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(MentalUser, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:50]


class ScaledFeedback(BaseModel, models.Model):
    scale = models.CharField(max_length=10, null=True)
    notes = models.TextField(null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.session.student.username} | Scale: {self.scale}"


class WebsiteFeedback(BaseModel, models.Model):
    feedbackDate = models.DateField()
    comment = models.TextField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.username} | Comment: {self.comment[0:50]}"


class Test(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)

    age_group_choices = [
        ('18_to_25', '18 to 25'),
        ('26_to_35', '26 to 35'),
        ('36_to_50', '36 to 50'),
        ('over_50', 'Over 50')
    ]
    age_group = models.CharField(max_length=10, choices=age_group_choices)
    symptoms_duration_choices = [
        ('less_than_3_months', 'Less than 3 months'),
        ('3_to_6_months', '3 to 6 months'),
        ('1_to_3_years', '1 to 3 years'),
        ('over_3_years', 'Over 3 years')
    ]
    symptoms_duration = models.CharField(max_length=20, choices=symptoms_duration_choices)
    level_of_functioning_choices = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]
    level_of_functioning = models.CharField(max_length=10, choices=level_of_functioning_choices)
    family_history_choices = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('unsure', 'Unsure')
    ]
    family_history = models.CharField(max_length=10, choices=family_history_choices)
    preferred_treatment_choices = [
        ('medication', 'Medication'),
        ('therapy', 'Therapy'),
        ('both', 'Both')
    ]
    preferred_treatment = models.CharField(max_length=10, choices=preferred_treatment_choices)

    symptoms_choices = [
        ('Depression',
         'Persistent feelings of hopelessness or emptiness, Loss of interest or pleasure in activities, Difficulty '
         'sleeping or focusing, and Changes in your appetite or weight.'),
        ('PTSD',
         'Thoughts or memories of a traumatic event, Dissociative symptoms, such as feeling detached from oneself or '
         'from reality, and Increased arousal, such as difficulty sleeping or being easily startled.'),
        ('Anxiety',
         'Excessive and persistent worry or fear, physical symptoms (can include restlessness, muscle tension, '
         'trembling, sweating, rapid heartbeat, shortness of breath), and Increased heart rate or breathing rapidly.'),
        ('Consultation', 'None of the answers.'),
    ]
    symptoms = models.CharField(max_length=25, choices=symptoms_choices)

    def __str__(self):
        return f"{self.user.username} | {self.symptoms}"
