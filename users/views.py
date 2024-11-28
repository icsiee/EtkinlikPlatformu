from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

from django.contrib.auth.views import PasswordResetView
from .forms import UsernameResetForm


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
            form.save(request.POST)
            return redirect('login')  # Parola sıfırlama işlemi başarıyla tamamlandığında login sayfasına yönlendir
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

from django.contrib.auth import logout
from django.shortcuts import redirect
@csrf_exempt

def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to the login page after logout



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages



# Get the custom user model
User = get_user_model()

@csrf_exempt
# Admin Dashboard View - Lists all users
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')  # Eğer admin değilse, ana sayfaya yönlendir
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})

@csrf_exempt

# Kullanıcı Düzenleme
@login_required
def edit_user(request, user_id):
    if not request.user.is_staff:
        return redirect('home')  # Eğer admin değilse, ana sayfaya yönlendir

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.is_active = request.POST['is_active'] == 'True'
        user.save()
        return redirect('admin_dashboard')

    return render(request, 'edit_user.html', {'user': user})

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event
from .forms import EventForm  # Assuming you will create a form for Event model
from django.contrib.auth.decorators import login_required

# View for listing all events
# views.py
from django.shortcuts import render, redirect
from .models import Event
from .forms import EventCreationForm

# Etkinlik Listeleme View'i
def event_list(request):
    events = Event.objects.all()
    return render(request, 'admin/event_list.html', {'events': events})

# Etkinlik Ekleme/Düzenleme View'i
from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required

@login_required  # Bu dekoratör, kullanıcının giriş yapmış olmasını zorunlu kılar
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)  # Etkinliği veritabanına kaydetmeden önce düzenleyelim
            event.created_by = request.user  # Oturum açmış kullanıcıyı 'created_by' alanına ata
            event.save()  # Etkinliği kaydet
            return redirect('event_list')  # Etkinlik listesine yönlendirme yap
    else:
        form = EventForm()
    return render(request, 'events/event_add.html', {'form': form})


# View for editing an event
@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')  # Redirect after successful edit
    else:
        form = EventForm(instance=event)
    return render(request, 'admin/event_form.html', {'form': form})

# View for deleting an event
@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')  # Redirect after deletion
    return render(request, 'admin/event_confirm_delete.html', {'event': event})

# views.py
from django.shortcuts import render, redirect
from .forms import EventCreationForm

def create_event(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')  # Başka bir sayfaya yönlendirebilirsiniz
    else:
        form = EventCreationForm()
    return render(request, 'create_event.html', {'form': form})

from django.shortcuts import render, redirect
from .models import Event  # Event modelini import edin

def event_create(request):
    if request.method == "POST":
        # Formdan gelen enlem ve boylam bilgilerini alın
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Yeni etkinlik kaydını oluşturun
        Event.objects.create(
            title=request.POST.get('title'),  # Etkinlik başlığı gibi diğer form verileri
            latitude=latitude,
            longitude=longitude
        )

        return redirect('event_list')  # Etkinlikler listesine yönlendirme

    return render(request, 'event_map.html')

from django.shortcuts import render

def select_event_location(request):
    if request.method == "POST":
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        # Veritabanına kaydetme işlemi burada yapılabilir
        # Event.objects.create(latitude=latitude, longitude=longitude)

        # Başka bir sayfaya yönlendirme (örneğin, etkinlik listeleme sayfası)
        return redirect('event_list')

    return render(request, 'events/select_event_location.html')



@csrf_exempt
def password_reset_view(request):
    if request.method == 'POST':
        form = UsernameResetForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)

            # Parola sıfırlama token'ı oluştur
            token = default_token_generator.make_token(user)
            uid = user.pk  # Kullanıcı ID'sini al

            # Şifre sıfırlama bağlantısını oluştur
            reset_url = f"{request.scheme}://{request.get_host()}/password_reset/{uid}/{token}/"

            # Kullanıcıya e-posta gönder
            send_mail(
                'Parola Sıfırlama Talebi',
                f'Parolanızı sıfırlamak için şu bağlantıya tıklayın: {reset_url}',
                'no-reply@example.com',
                [user.email],
                fail_silently=False,
            )

            messages.success(request, "E-posta adresinize parola sıfırlama bağlantısı gönderildi.")
            return redirect('login')  # Parola sıfırlama linki gönderildikten sonra login sayfasına yönlendir
    else:
        form = UsernameResetForm()
    return render(request, 'users/password_reset.html', {'form': form})

def password_reset_confirm_view(request, uidb64, token):
    try:
        # UID'yi ve token'ı çözümle
        uid = uidb64
        user = get_user_model().objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            if request.method == 'POST':
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('login')  # Parola başarıyla sıfırlandığında login sayfasına yönlendir
            else:
                form = SetPasswordForm(user)
            return render(request, 'users/password_reset_confirm.html', {'form': form})
        else:
            messages.error(request, "Geçersiz veya süreli dolmuş parola sıfırlama bağlantısı.")
            return redirect('password_reset')
    except Exception as e:
        messages.error(request, "Geçersiz kullanıcı veya token.")
        return redirect('password_reset')


