from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from users.models import User  # Kullanıcı modelini import edin
from django.contrib.auth.models import BaseUserManager
from .models import User
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Parola şifrelenerek kaydedilir
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


from django.contrib.auth import get_user_model
@csrf_exempt

def authenticate(request, username=None, password=None):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):  # Parola doğru mu?
            return user
    except User.DoesNotExist:
        return None

@csrf_exempt

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Süper kullanıcıyı kontrol et
            login(request, user)
            return redirect('admin:index')  # Admin paneline yönlendir
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return render(request, 'admin_login.html')  # Hata mesajıyla giriş sayfasına geri dön

@csrf_exempt

def create_superuser(self, username, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    return self.create_user(username, email, password, **extra_fields)


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Kullanıcıyı doğrulama
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Eğer kullanıcı bir adminse (is_superuser = True), giriş yapmasına izin verme
            if user.is_superuser:
                messages.error(request, "Admin kullanıcıları giriş yapamaz.")
                return redirect('login')  # Admin kullanıcısının girişini engelle

            login(request, user)
            return redirect('user_dashboard')  # Başarılı giriş sonrası kullanıcı paneline yönlendirme
        else:
            # Şifre yanlışsa hata mesajı göster
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return redirect('login')  # Hatalı girişte tekrar giriş sayfasına yönlendir

    return render(request, "login.html")


# Kullanıcı Giriş Fonksiyonu
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User

@csrf_exempt

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_dashboard')  # Giriş sonrası yönlendirme
        else:
            # Giriş başarısız olursa hata mesajı göster
            return render(request, 'login.html', {'error': 'Geçersiz kullanıcı adı veya şifre'})
    return render(request, 'login.html')
@csrf_exempt

def user_dashboard(request):
    return render(request, 'user_dashboard.html')  # Kullanıcı panelini render et


# Kayıt Olma Fonksiyonu

from .forms import CustomUserCreationForm
@csrf_exempt

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Şifreyi şifreli olarak kaydediyoruz
            user.save()
            messages.success(request, "Kayıt başarılı! Şimdi giriş yapabilirsiniz.")
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

@csrf_exempt

# Parola Sıfırlama Fonksiyonu
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Parola sıfırlama talimatları gönderildi!")
            return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'users/password_reset.html', {'form': form})

@csrf_exempt

# Kullanıcı Dashboard
def user_dashboard(request):
    return render(request, 'user_dashboard.html')  # User dashboard screen

@csrf_exempt

# Çıkış Yapma Fonksiyonu
def logout_view(request):
    logout(request)
    return redirect('login')
@csrf_exempt

def admin_dashboard_view(request):
    return render(request, 'admin_dashboard.html')  # Yönetici paneli ekranı
@csrf_exempt

def home_view(request):
    return render(request, 'login.html')  # Kullanıcıların gördüğü ana ekran
