# users/views.py



from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages


# Giriş sayfası
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_admin_login = 'admin_login' in request.POST  # Admin login checkbox'ını kontrol ediyoruz

        # Admin Girişi Kontrolü
        if is_admin_login:  # Admin giriş kontrolü
            if username == 'iclal' and password == '1234':  # Admin kullanıcı adı ve şifresi kontrolü
                user = authenticate(request, username=username, password=password)
                if user is not None and user.is_superuser:  # Admin yetkisini kontrol et
                    login(request, user)
                    return redirect('admin:index')  # Admin paneline yönlendir
                else:
                    messages.error(request, 'Geçersiz admin giriş bilgileri.')
                    return render(request, 'users/login.html')

            else:
                messages.error(request, 'Geçersiz admin kullanıcı adı veya şifre.')
                return render(request, 'users/login.html')

        # Normal Kullanıcı Girişi
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Ana sayfaya veya kullanıcı paneline yönlendir
        else:
            messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
            return render(request, 'users/login.html')  # Hata mesajı ile giriş sayfasına dön

    # GET isteği: Boş bir formla sayfa yüklenir
    return render(request, 'users/login.html')


from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model


def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    admin_user = get_user_model().objects.filter(is_superuser=True).first()

    if form.is_valid():
        form.save()
        return redirect('login')  # Başarıyla kayıt olduktan sonra login sayfasına yönlendir

    return render(request, 'signup.html', {
        'form': form,
        'admin_email': admin_user.email if admin_user else 'Admin not found'
    })


# Kayıt sayfası
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # Kaydı kaydet
            messages.success(request, "Hesap başarıyla oluşturuldu!")
            return redirect('login')  # Başarıyla kaydedildikten sonra giriş sayfasına yönlendir
        else:
            messages.error(request, "Hesap oluşturulamadı. Lütfen formu kontrol edin.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

# Parola sıfırlama sayfası
def password_reset_view(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(request.POST)
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

# views.py

from django.shortcuts import render

def user_dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'users/user_dashboard.html')  # Kullanıcıya kişisel sayfayı göster
    else:
        return redirect('login')  # Eğer kullanıcı oturum açmamışsa login sayfasına yönlendir

# views.py

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')  # Çıkış yapınca login sayfasına yönlendir




