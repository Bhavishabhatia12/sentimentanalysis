from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    Brand_name = forms.CharField(max_length=101)
    domain_name = forms.CharField(max_length=101)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','Brand_name', 'domain_name', 'email', 'password1', 'password2']