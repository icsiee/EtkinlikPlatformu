from django import forms
from .models import Event, User, Interest


class EventForm(forms.ModelForm):
    time = forms.TimeField(
        input_formats=['%H:%M'],  # Beklenen format: HH:MM
        widget=forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        required=False
    )
    category = forms.ChoiceField(
        choices=Event.CATEGORY_CHOICES,  # Kategori seçenekleri
        widget=forms.Select(attrs={'class': 'form-control'}),  # Combobox için Select widget'ı
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'duration', 'category']

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Adds a date picker to the form
        required=True,
        label='Etkinlik Tarihi'
    )


# users/forms.py
class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'location', 'latitude', 'longitude', 'category']  # created_by formda yok

    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True,
        label='Etkinlik Tarihi'
    )


from django import forms
from .models import User, Interest

class CustomUserCreationForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),  # Adds a date picker to the form
        required=True,
        label='Doğum Tarihi'
    )

    name = forms.CharField(max_length=100, required=True, label='Adınız')
    surname = forms.CharField(max_length=100, required=True, label='Soyadınız')
    gender = forms.ChoiceField(choices=[('K', 'Kadın'), ('E', 'Erkek')], required=False, label='Cinsiyet')
    email = forms.EmailField(required=True, label='E-posta Adresi')
    phone_number = forms.CharField(max_length=15, required=True, label='Telefon Numarası')
    profile_picture = forms.ImageField(required=False, label='Profil Resmi')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Şifre')

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'surname', 'birth_date', 'gender', 'email', 'phone_number', 'profile_picture', 'interests']



# users/forms.py
class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = ['name', 'description']


