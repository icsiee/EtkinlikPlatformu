from django.contrib.auth import authenticate, login
from .models import Event, Participant
from django.contrib.auth import logout
from .models import Event, User
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
User = get_user_model()


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
            return redirect('login')
        else:
            messages.error(request, "Geçersiz kullanıcı adı veya şifre.")
            return redirect('login')

    return render(request, 'login.html')  # Admin login page


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

        username=request.POST.get("username")
        password=request.POST.get("password")
        print(username,password)
        user=User.objects.filter(username=username).first()
        print(user)
        if user:
            user.set_password(password)
            user.save()
        messages.success(request, "Parola sıfırlama talimatları gönderildi!")
        return redirect('login')
    else:
        form = PasswordResetForm()

    return render(request, 'users/password_reset.html', )


def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    if event not in user.events.all():
        user.events.add(event)
        handle_event_join(user, event)
        handle_first_join_event(user, event)

    return redirect('user_dashboard')


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to the login page after logout



from django.shortcuts import render
from .models import Event, Points
from django.db import models


from django.db.models import Sum
from .models import Event, Points

def user_dashboard(request):
    user = request.user

    # Kullanıcının oluşturduğu etkinlikler
    created_events = Event.objects.filter(created_by=user)

    # Kullanıcının katılabileceği etkinlikler (onaylanmış, kendisinin oluşturmadığı)
    available_events = Event.objects.filter(status='approved').exclude(created_by=user)

    # Kullanıcının toplam puanı
    total_points = Points.objects.filter(user=user).aggregate(total=Sum('score'))['total'] or 0

    # Kullanıcının katıldığı etkinlik sayısı
    user_events_count = user.events.count()

    # Kullanıcının admin tarafından onaylanmış etkinliklerinin sayısı
    user_created_events_count = created_events.filter(status='approved').count()

    # Bağlama verileri (context)
    context = {
        'created_events': created_events,
        'available_events': available_events,
        'total_points': total_points,
        'user_events_count': user_events_count,
        'user_created_events_count': user_created_events_count,
    }

    return render(request, 'users/user_dashboard.html', context)



@csrf_exempt
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')  # Eğer admin değilse, ana sayfaya yönlendir
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users})




from django.db import IntegrityError

@csrf_exempt
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        new_username = request.POST.get('username')

        # Kullanıcı adı değiştiyse, benzersiz olup olmadığını kontrol et
        if new_username != user.username:
            try:
                User.objects.get(username=new_username)  # Aynı kullanıcı adı var mı kontrol et
                return render(request, 'edit_user.html', {'user': user, 'error': 'Bu kullanıcı adı zaten alınmış.'})
            except User.DoesNotExist:
                pass  # Kullanıcı adı mevcut değilse geç

        user.username = new_username
        user.email = request.POST.get('email')
        user.is_active = request.POST.get('is_active') == 'True'
        user.phone_number = request.POST.get('phone_number')
        user.birth_date = request.POST.get('birth_date')
        user.gender = request.POST.get('gender')

        # Profil resmini güncelle
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        try:
            user.save()  # Kullanıcıyı kaydet
        except IntegrityError:
            return render(request, 'edit_user.html', {'user': user, 'error': 'Veritabanı hatası! Lütfen tekrar deneyin.'})

        return redirect('admin_dashboard')  # Düzenlenen kullanıcı detayına yönlendirme

    return render(request, 'edit_user.html', {'user': user})


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


    # Onay işleminden sonra etkinlik listesine yönlendir
    return redirect('event_list')  # 'event_list' URL adı ile yönlendir


def reject_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.status = 'rejected'
    event.save()
    return redirect('event_list')



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



def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')

    return render(request, 'events/delete_event.html', {'event': event})



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
            return redirect('event_list')  # Etkinlik listesi sayfasına yönlendir
    else:
        form = EventForm()
    return render(request, 'users/event_map.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import Event

def event_detail(request, event_id):
    # Belirtilen etkinliği al veya 404 döndür
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'users/event_detail.html', {'event': event})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event
# users/views.py


def update_event(request, event_id):
    # Etkinliği al, ancak yalnızca oluşturan kullanıcı erişebilsin
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Etkinlik başarıyla güncellendi!')
            return redirect('user_dashboard')  # Güncelleme sonrası dashboard'a yönlendir
    else:
        form = EventForm(instance=event)

    return render(request, 'users/update_event.html', {'form': form, 'event': event})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import EventForm, CustomUserCreationForm, InterestForm
from .models import Event


def user_event_map(request, event_id=None):
    """
    Kullanıcılar için etkinlik ekleme veya düzenleme işlemleri.
    Eğer event_id verilmişse düzenleme, verilmemişse yeni etkinlik oluşturma.
    """
    if event_id:
        event = get_object_or_404(Event, id=event_id, created_by=request.user)
        form = EventForm(request.POST or None, instance=event)
    else:
        event = None
        form = EventForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.created_by = request.user

            # Latitude ve longitude değerlerini formdan al
            new_event.latitude = request.POST.get('latitude')
            new_event.longitude = request.POST.get('longitude')
            new_event.location = f"{new_event.latitude}, {new_event.longitude}"
            new_event.save()


            return redirect('user_dashboard')  # Kullanıcı dashboard'una yönlendirme

    return render(request, 'users/user_event_map.html', {
        'form': form,
        'event': event
    })


from django.shortcuts import render, get_object_or_404
from .models import User, Participant, Event


def user_detail(request, user_id):
    # Kullanıcıyı ID'ye göre buluyoruz
    user = get_object_or_404(User, id=user_id)

    # Kullanıcının katıldığı etkinlikleri alıyoruz
    user_participations = Participant.objects.filter(user=user).select_related('event')

    # Kullanıcının oluşturduğu etkinlikleri alıyoruz
    created_events = Event.objects.filter(created_by=user)

    # Kullanıcının katıldığı etkinliklerin detaylarını ve oluşturduğu etkinlikleri göndereceğiz
    return render(request, 'user_detail.html', {
        'user': user,
        'user_participations': user_participations,
        'created_events': created_events,
    })

# views.py
from django.shortcuts import render, redirect
from .models import Interest

# İlgi Alanlarını Listeleme
def user_interests(request):
    interests = Interest.objects.all()  # Tüm ilgi alanlarını al
    return render(request, 'user_interests.html', {'interests': interests})

def add_interest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            form.save()  # Yeni ilgi alanı kaydet
            return redirect('user_interests')  # İlgi alanları sayfasına yönlendir
    else:
        form = InterestForm()
    return render(request, 'add_interest.html', {'form': form})


def delete_interest(request, interest_id):
    # İlgili ilgi alanını al
    interest = get_object_or_404(Interest, id=interest_id)

    # Silme işlemi
    if request.method == 'POST':
        interest.delete()
        return redirect('user_interests')  # İlgi alanları sayfasına geri yönlendir

    return render(request, 'user_interests.html', {'interest': interest})


def edit_interest(request, interest_id):
    interest = get_object_or_404(Interest, id=interest_id)

    if request.method == 'POST':
        form = InterestForm(request.POST, instance=interest)
        if form.is_valid():
            form.save()
            return redirect('user_interests')  # Düzenleme sonrası ilgi alanları sayfasına yönlendir
    else:
        form = InterestForm(instance=interest)

    return render(request, 'users/edit_interest.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event

def dashboard(request):
    created_events = Event.objects.filter(created_by=request.user)
    available_events = Event.objects.exclude(created_by=request.user)
    user_events_count = created_events.count()
    user_created_events_count = created_events.count()

    context = {
        'created_events': created_events,
        'available_events': available_events,
        'user_events_count': user_events_count,
        'user_created_events_count': user_created_events_count,
        'total_points': calculate_user_points(request.user),  # Burada çağrılıyor
    }
    return render(request, 'users/user_dashboard.html', context)

def resubmit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if event.status == 'rejected':
        event.status = 'pending'  # Durumu "Onay Bekliyor" olarak güncelle
        event.save()
        messages.success(request, f"'{event.name}' etkinliği tekrar onaya gönderildi.")
    else:
        messages.error(request, "Bu etkinliği tekrar gönderemezsiniz.")

    return redirect('user_dashboard')


def calculate_user_points(user):
    total_points = user.user_points.aggregate(total=models.Sum('score'))['total'] or 0
    joined_events_count = user.events.count()
    created_events_count = user.created_events.filter(status='approved').count()

    return {
        'total_points': total_points,
        'joined_events_count': joined_events_count,
        'created_events_count': created_events_count,
    }

def add_points(user, score, point_type):
    Points.objects.create(user=user, score=score, point_type=point_type)

def handle_first_join_event(user, event):
    if user.events.count() == 0:  # Kullanıcının ilk etkinliği
        add_points(user, 20, 'first_join_bonus')

def handle_event_join(user, event):
    add_points(user, 10, 'join_event')


def handle_approved_event(event):
    if event.status == 'approved':
        add_points(event.created_by, 15, 'create_event')




def rejected_events(request):
    # Kullanıcı tarafından oluşturulmuş reddedilen etkinlikleri al
    rejected_events = Event.objects.filter(created_by=request.user, status='rejected')

    context = {
        'rejected_events': rejected_events,
    }
    return render(request, 'users/rejected_events.html', context)


