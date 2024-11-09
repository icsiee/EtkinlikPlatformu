from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'surname', 'birth_date', 'gender', 'email', 'phone_number', 'interests', 'profile_picture', 'password1', 'password2']
