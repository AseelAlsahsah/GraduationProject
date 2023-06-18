from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm
from .models import Student, Consultant, WebsiteFeedback, Test, ScaledFeedback
from django import forms
import datetime


def validate_email_domain(value):
    """
    Custom validator to ensure that the email address
    belongs to the domain 'ju.edu.jo'.
    """
    domain = value.split('@')[1]
    if domain != 'ju.edu.jo':
        raise forms.ValidationError('Email address must belong to the domain ju.edu.jo')


class StudentForm(ModelForm):
    email = forms.EmailField(required=True,
                             validators=[validate_email_domain],
                             widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))

    class Meta:
        model = Student
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        }


class ConsultantForm(ModelForm):
    MAJOR_CHOICES = [
        ('Depression', 'Depression'),
        ('Anxiety', 'Anxiety'),
        ('PTSD', 'PTSD'),
        ('Consultation', 'Consultation'),
    ]

    email = forms.EmailField(required=True,
                             validators=[validate_email_domain],
                             widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    major = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=MAJOR_CHOICES,
    )
    profilePicture = forms.ImageField(required=True,
                                      widget=forms.FileInput(attrs={'accept': 'image/*'}))
    resume = forms.FileField(required=True,
                             widget=forms.FileInput(attrs={'accept': 'application/pdf'}))

    class Meta:
        model = Consultant
        fields = ('username', 'email', 'password', 'major', 'profilePicture', 'resume')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        }

    def __init__(self, *args, **kwargs):
        self.consultant = kwargs.pop('consultant', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False  # User status is set to False by default
        user.major = ', '.join(self.cleaned_data['major'])
        if commit:
            user.save()
        return user


class WebsiteFeedbackForm(ModelForm):
    class Meta:
        model = WebsiteFeedback
        fields = ['comment']
        widgets = {
            'comment': forms.TextInput(attrs={'placeholder': 'Enter your feedback'}),
        }

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.student = self.student
        instance.feedbackDate = datetime.date.today()  # get the current date
        if commit:
            instance.save()
        return instance


class EditProfile(UserChangeForm):
    profilePicture = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={'accept': 'image/*', 'style': 'padding-left:260px; border: 0;'}))

    class Meta:
        model = Consultant
        fields = ('username', 'profilePicture')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter new username'}),
        }


class TestForm(forms.ModelForm):
    age_group = forms.ChoiceField(choices=Test.age_group_choices, widget=forms.RadioSelect)
    symptoms_duration = forms.ChoiceField(choices=Test.symptoms_duration_choices, widget=forms.RadioSelect)
    level_of_functioning = forms.ChoiceField(choices=Test.level_of_functioning_choices, widget=forms.RadioSelect)
    family_history = forms.ChoiceField(choices=Test.family_history_choices, widget=forms.RadioSelect)
    preferred_treatment = forms.ChoiceField(choices=Test.preferred_treatment_choices, widget=forms.RadioSelect)
    symptoms = forms.ChoiceField(choices=Test.symptoms_choices, widget=forms.RadioSelect)

    class Meta:
        model = Test
        fields = ['age_group', 'symptoms_duration', 'level_of_functioning', 'family_history', 'preferred_treatment',
                  'symptoms']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user


class ScaledFeedbackForm(ModelForm):
    class Meta:
        model = ScaledFeedback
        fields = ['scale', 'notes']
        widgets = {
            'scale': forms.Select(attrs={'id': 'stages'}),
            'notes': forms.Textarea(attrs={'id': 'notes', 'rows': 10, 'cols': 30}),
        }

