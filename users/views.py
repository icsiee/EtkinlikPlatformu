from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

from .forms import CustomUserCreationForm

User = get_user_model()

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden

@csrf_exempt

# User login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None and not user.is_superuser:  # User is not an admin
            login(request, user)
            return redirect('user_dashboard')  # Redirect to the home or dashboard page
        elif user is not None and user.is_superuser:  # User is an admin trying to log in as a regular user
            messages.error(request, "Admin girişi sadece admin panelinde yapılabilir.")
            return redirect('user_login')
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return redirect('user_login')

    return render(request, 'login.html')  # Render the login page

@csrf_exempt

# Admin login view
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:  # Admin login check
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        elif user is not None and not user.is_superuser:  # Non-admin user trying to log in as admin
            messages.error(request, "Kullanıcı girişi sadece kullanıcı panelinde yapılabilir.")
            return redirect('admin_login')
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return redirect('admin_login')

    return render(request, 'admin_login.html')  # Admin login page


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:  # Admin kontrolü
                login(request, user)
                return redirect('admin_dashboard')  # Admin paneline yönlendir
            else:
                login(request, user)
                return redirect('user_dashboard')  # Normal kullanıcı yönlendirme
        else:
            return render(request, 'login.html', {'error': 'Hatalı kullanıcı adı veya şifre.'})
    return render(request, 'login.html')


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
def user_dashboard(request):
    return render(request, 'user_dashboard.html')  # User dashboard ekranı


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')  # Admin paneli ekranı


