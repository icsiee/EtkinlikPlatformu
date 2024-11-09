from django import forms
from .models import User, Interest

class CustomUserCreationForm(forms.ModelForm):
    # İlgili ilgi alanlarını kullanıcıya sunmak için CheckboxSelectMultiple kullanıyoruz
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    # Doğum tarihi için tarih widget'ı ekliyoruz (sınırlama yok)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True,
        label='Doğum Tarihi'
    )

    # Zorunlu alanlar için mesajlar ekliyoruz
    name = forms.CharField(max_length=100, required=True, label='Adınız')
    surname = forms.CharField(max_length=100, required=True, label='Soyadınız')
    gender = forms.ChoiceField(choices=[('K', 'Kadın'), ('E', 'Erkek')], required=False, label='Cinsiyet')
    email = forms.EmailField(required=True, label='E-posta Adresi')
    phone_number = forms.CharField(max_length=15, required=True, label='Telefon Numarası')

    # Profil resmi isteğe bağlı (null olabilir)
    profile_picture = forms.ImageField(required=False, label='Profil Resmi')

    # Şifreyi gizli alıyoruz (uzunluk sınırlaması yok)
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Şifre')

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'surname', 'birth_date', 'gender', 'email', 'phone_number',
                  'profile_picture', 'interests']

    def clean_username(self):
        # Kullanıcı adı kontrolü: Aynı kullanıcı adı varsa hata veriyoruz
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı zaten alınmış.")
        return username

    def clean_email(self):
        # E-posta adresi kontrolü: Aynı e-posta varsa hata veriyoruz
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return email

from django import forms
from .models import User, Interest

class UserInterestForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(queryset=Interest.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = User
        fields = ['interests']