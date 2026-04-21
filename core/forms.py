from django import forms
from .models import Visit, Profile, Location
from django.contrib.auth.models import User


class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['profile', 'location', 'visit_type', 'hours_logged']
        widgets = {
            'profile': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'visit_type': forms.RadioSelect(),
            'hours_logged': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'step': '0.5'
            }),
        }
        labels = {
            'profile': 'Who are you?',
            'location': 'Where are you?',
            'visit_type': 'What are you doing today?',
            'hours_logged': 'Hours Logged (only required if volunteering)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active locations in the dropdown
        self.fields['location'].queryset = Location.objects.filter(is_active=True).order_by('name')
        self.fields['profile'].queryset = Profile.objects.all().order_by('last_name')

    def clean(self):
        cleaned = super().clean()
        visit_type = cleaned.get('visit_type')
        hours = cleaned.get('hours_logged')

        if visit_type == 'Volunteered':
            if not hours or hours <= 0:
                raise forms.ValidationError(
                    "Please enter a valid number of hours greater than 0 when volunteering.")
        else:
            cleaned['hours_logged'] = None
        return cleaned
    
class SignupForm(forms.Form):
    ACCOUNT_TYPES = [
        ('Volunteer', 'Volunteer'),
        ('Community Member', 'Community Member'),
    ]

    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPES, widget=forms.Select(
        attrs={'class': 'form-select'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("That username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if Profile.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords don't match.")
        return cleaned