from django import forms
from .models import JournalEntry, UserCreds

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserCreds
        fields = ['email', 'password', 'first_name', 'phone_number']

class TherapistSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserCreds
        fields = ['email', 'password', 'first_name', 'phone_number']

class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = JournalEntry
        fields = ['entry_text','image']
