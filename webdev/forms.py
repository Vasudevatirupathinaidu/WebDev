
from django import forms
from django.contrib.auth.forms import PasswordResetForm

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'input'}))

    password1 = forms.CharField(label="New password", widget=forms.PasswordInput(attrs={'class': 'input'}))

    password2 = forms.CharField(label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'input'}))