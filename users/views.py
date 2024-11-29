
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from .models import User, Event
from .forms import CustomUserCreationForm
from .forms import EventCreationForm
from django.shortcuts import render, get_object_or_404, redirect

User = get_user_model()

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


from django.shortcuts import get_object_or_404, redirect
from .models import Event, Participant


def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    # Kullanıcıyı etkinliğe katılanlar listesine ekle
    if not Participant.objects.filter(user=user, event=event).exists():
        Participant.objects.create(user=user, event=event)

    return redirect('user_dashboard')  # Kullanıcıyı dashboard'a yönlendir


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
from .models import Event, User
from django.contrib import messages


from django.shortcuts import render
from .models import Event

def user_dashboard(request):
    user = request.user
    # Get the events created by the user
    created_events = Event.objects.filter(created_by=user)

    # Get the events the user has joined
    user_events_count = user.events.count()  # This will count events the user has joined
    user_created_events_count = created_events.count()  # This will count events the user has created
    total_points = user.points  # Assuming you have points field for the user

    # Get approved events that the user hasn't created
    available_events = Event.objects.filter(status='approved').exclude(created_by=user)

    context = {
        'user_events_count': user_events_count,
        'user_created_events_count': user_created_events_count,
        'total_points': total_points,
        'created_events': created_events,
        'available_events': available_events,
    }

    return render(request, 'users/user_dashboard.html', context)



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


from django.shortcuts import render
from .models import Event

from django.shortcuts import render
from .models import Event

def event_list(request):
    # Kullanıcının onay bekleyen etkinlikleri ve onaylanan etkinlikleri listelemesi
    pending_events = Event.objects.filter(status='pending')
    approved_events = Event.objects.filter(status='approved')

    # Bu view'de sadece onaylı ve onay bekleyen etkinlikler listelenir
    return render(request, 'admin/event_list.html', {
        'pending_events': pending_events,
        'approved_events': approved_events,
    })

def delete_event(request, event_id):
    # Etkinliği silmek için bir fonksiyon
    event = Event.objects.get(id=event_id)
    if event.status == 'rejected':  # Eğer etkinlik reddedildiyse
        event.delete()  # Etkinlik veritabanından silinir
    return redirect('admin/event_list')  # Etkinlikler sayfasına yönlendirme


from django.contrib import messages
from django.shortcuts import redirect
from .models import Event, Points

from .models import Points

from django.shortcuts import redirect
from .models import Event, Points


from django.shortcuts import redirect
from django.contrib import messages

def approve_event(request, event_id):
    # Etkinliği al
    event = Event.objects.get(id=event_id)

    # Etkinliği onayla
    event.status = 'approved'
    event.save()

    # Etkinliği oluşturan kullanıcıyı al
    user = event.created_by

    # Kullanıcı admin değilse puan ekle
    if not user.is_admin:  # Admin kullanıcıyı kontrol et
        points_entry = Points(user=user, score=15)
        points_entry.save()

    # Etkinlik onaylandığında kullanıcıya başarı mesajı göster
    messages.success(request, 'Etkinlik başarıyla onaylandı.')

    # Onay işleminden sonra etkinlik listesine yönlendir
    return redirect('event_list')  # 'event_list' URL adı ile yönlendir



def reject_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.status = 'rejected'
    event.save()
    return redirect('event_list')

# Etkinlik Ekleme/Düzenleme View'i
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

# users/views.py
# users/views.py
from django.shortcuts import render, redirect
from .forms import EventCreationForm
from .models import Event
from django.contrib.auth.decorators import login_required

@login_required
def event_add(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)  # Veritabanına kaydetmeden önce bir nesne oluştur
            event.created_by = request.user  # Etkinliği oluşturan kullanıcıyı ata
            event.save()  # Etkinliği kaydet
            return redirect('users:events_dashboard')  # Başarılıysa yönlendirme yap
    else:
        form = EventCreationForm()
    return render(request, 'users/event_form.html', {'form': form})


# View for editing an event
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event
from .forms import EventForm


# Etkinlik düzenleme view
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Etkinlik başarıyla güncellendi!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form, 'event': event})


# Etkinlik silme view
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, "Etkinlik başarıyla silindi!")
        return redirect('event_list')

    return render(request, 'events/delete_event.html', {'event': event})


# views.py
from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event
from .forms import EventForm

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Etkinliği oluşturan kullanıcıyı ata
            # Latitude ve longitude değerlerini formdan al
            event.latitude = request.POST.get('latitude')
            event.longitude = request.POST.get('longitude')
            event.location = f"{event.latitude}, {event.longitude}"  # Konum bilgisini birleştir
            event.save()
            # Kullanıcıya başarı mesajı gönder
            messages.success(request, 'Etkinlik başarıyla kaydedildi!')
            return redirect('event_list')  # Etkinlik listesi sayfasına yönlendir
    else:
        form = EventForm()
    return render(request, 'users/event_map.html', {'form': form})