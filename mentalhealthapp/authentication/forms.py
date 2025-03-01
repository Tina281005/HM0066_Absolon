from django import forms
from .models import UserCreds

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
