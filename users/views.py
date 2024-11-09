# users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User  # User modelini import et


# Giriş sayfası
# Giriş sayfası

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordResetForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import User  # User modelini import et


# Giriş sayfası
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Admin kontrolü
        if username == 'iclal' and password == '1234':
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_superuser:  # Eğer adminse
                login(request, user)
                return redirect('admin_dashboard')  # Admin paneline yönlendir
            else:
                # Admin değilse veya geçersiz giriş
                return render(request, 'users/login.html', {'error': 'Geçersiz giriş. Admin değil veya yanlış bilgi.'})

        # Diğer kullanıcılar için normal giriş işlemi
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Kullanıcıyı ana sayfaya yönlendir
        else:
            return render(request, 'users/login.html', {'error': 'Geçersiz kullanıcı adı veya parola.'})

    return render(request, 'users/login.html')


# Admin sayfası
def admin_dashboard(request):
    users = User.objects.all()  # Tüm kullanıcıları çekiyoruz
    return render(request, 'users/admin_dashboard.html', {'users': users})





# Kayıt sayfası
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

# Parola sıfırlama sayfası
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Parola sıfırlama işlemi başarıyla tamamlandığında login sayfasına yönlendir
    else:
        form = PasswordResetForm()
    return render(request, 'users/password_reset.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})