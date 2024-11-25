from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import PasswordResetForm
from .forms import CustomUserCreationForm
from users.models import User  # Kullanıcı modelini import edin

from django.contrib.auth.models import BaseUserManager

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

def authenticate(request, username=None, password=None):
    User = get_user_model()
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):  # Parola doğru mu?
            return user
    except User.DoesNotExist:
        return None


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Süper kullanıcıyı kontrol et
            login(request, user)
            # Mesajları temizle
            list(messages.get_messages(request))
            return redirect('admin:index')  # Admin paneline yönlendir
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return render(request, 'admin_login.html')  # Hata mesajıyla giriş sayfasına geri dön

    return render(request, 'admin_login.html')  # GET isteğinde giriş sayfasını göster


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            # Kullanıcıyı veritabanından alıyoruz
            user = User.objects.get(username=username)

            # Kullanıcı varsa, şifreyi kontrol ediyoruz
            if user.check_password(password):
                # Şifre doğruysa giriş yap
                login(request, user)
                messages.success(request, f"Merhaba, {user.username}!")
                return redirect('user_dashboard')  # Başarılı giriş sonrası yönlendirme
            else:
                # Şifre yanlışsa
                messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
                return redirect('login')  # Hatalı girişte tekrar giriş sayfasına yönlendir
        except User.DoesNotExist:
            # Kullanıcı bulunamazsa
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return redirect('login')  # Hatalı girişte tekrar giriş sayfasına yönlendir

    return render(request, "login.html")


# Kullanıcı Giriş Fonksiyonu
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Kullanıcıyı authenticate et
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # Kullanıcıyı giriş yapmış say
            messages.success(request, f"Merhaba, {user.username}!")
            return redirect('user_dashboard')  # Giriş başarılı, dashboard'a yönlendir
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return redirect('login')  # Hatalı girişte tekrar giriş sayfasına yönlendir

    return render(request, 'login.html')


from django.shortcuts import render

def user_dashboard(request):
    return render(request, 'user_dashboard.html')  # Kullanıcı panelini render et


# Kayıt Olma Fonksiyonu
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Kullanıcı var mı diye kontrol et
        if get_user_model().objects.filter(username=username).exists():
            messages.error(request, "Bu kullanıcı adı zaten var.")
            return redirect('signup')  # Hata durumunda tekrar kayıt sayfasına dön

        # Yeni kullanıcıyı oluştur
        user = get_user_model().objects.create_user(username=username, password=password, email=email)

        # Kullanıcı kaydının başarılı olduğunu kontrol et
        if user:
            messages.success(request, f"Hoş geldiniz, {user.username}!")
            return redirect('login')  # Başarıyla kaydedilen kullanıcıyı login sayfasına yönlendir
        else:
            messages.error(request, "Kayıt sırasında bir hata oluştu.")
            return redirect('signup')  # Hata durumunda tekrar kayıt sayfasına dön

    return render(request, 'signup.html')


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


# Kullanıcı Dashboard
def user_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'users/user_dashboard.html')
    else:
        return redirect('login')


# Çıkış Yapma Fonksiyonu
def logout_view(request):
    logout(request)
    return redirect('login')
