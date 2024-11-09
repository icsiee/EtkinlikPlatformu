from django import forms
from .models import User, Interest


class CustomUserCreationForm(forms.ModelForm):
    # İlgili ilgi alanlarını kullanıcıya sunmak için CheckboxSelectMultiple kullanıyoruz
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'surname', 'birth_date', 'gender', 'email', 'phone_number',
                  'profile_picture']

    password = forms.CharField(widget=forms.PasswordInput)  # Şifreyi gizli alıyoruz
