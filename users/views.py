from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt

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


from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

@csrf_exempt

def password_reset_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('password')

        # Kullanıcıyı bulmaya çalış
        try:
            user = User.objects.get(username=username)

            # Yeni şifreyi güncelle
            user.password = make_password(new_password)
            user.save()

            messages.success(request, "Parola başarıyla sıfırlandı!")
            return redirect('login')  # Giriş sayfasına yönlendir

        except User.DoesNotExist:
            messages.error(request, "Kullanıcı adı bulunamadı. Lütfen geçerli bir kullanıcı adı girin.")
            return redirect('password_reset')  # Parola sıfırlama sayfasına geri döner

    return render(request, 'users/password_reset.html')


@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def user_logout(request):
    logout(request)
    return redirect('user_login')  # Redirect to the login page after logout



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



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import User

@csrf_exempt
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')  # Eğer admin değilse, ana sayfaya yönlendir

    users = User.objects.all()
    user_data = []

    # Kullanıcılar için toplam puanları ve etkinlik bilgilerini hesapla
    for user in users:
        points_data = calculate_user_points(user)  # Her kullanıcı için puan verilerini hesapla
        user_data.append({
            'user': user,
            'total_points': points_data['total_points'],
            'joined_events_count': points_data['joined_events_count'],
            'created_events_count': points_data['created_events_count'],
        })

    return render(request, 'admin_dashboard.html', {'user_data': user_data})



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


from django.utils import timezone

def approve_event(request, event_id):
    # Kullanıcının yönetici olup olmadığını kontrol et
    if not request.user.is_staff:
        messages.error(request, "Bu işlemi gerçekleştirme yetkiniz yok.")
        return redirect('user_dashboard')

    # Etkinlik bulunur
    event = get_object_or_404(Event, id=event_id)

    # Etkinlik durumu onaylandı
    event.status = 'approved'
    event.save()

    # Etkinliği oluşturan kullanıcıya 15 puan ekle
    creator = event.created_by
    add_points(creator, 15, 'create_event')

    # Etkinlik için bir mesaj oluştur
    Message.objects.create(
        sender=request.user,  # Yönetici mesajı gönderen
        event=event,
        text=f"{event.name} etkinliği onaylandı ve 15 puan kazandınız.",
        sent_at=timezone.now()
    )

    messages.success(request, f"{event.name} etkinliği başarıyla onaylandı.")
    return redirect('admin_dashboard')  # Yönetici paneline yönlendirin

def add_points(user, points, point_type):
    # Kullanıcıya puan ekleyen fonksiyon
    Points.objects.create(
        user=user,
        score=points,
        point_type=point_type
    )



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

from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from .models import Event
from django.contrib.auth.decorators import login_required

@login_required  # Kullanıcının giriş yapmış olmasını zorunlu kılar
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Etkinliği oluşturan kullanıcıyı ata
            # Latitude ve longitude değerlerini formdan al
            event.latitude = request.POST.get('latitude')
            event.longitude = request.POST.get('longitude')
            if event.latitude and event.longitude:
                event.location = f"{event.latitude}, {event.longitude}"  # Konum bilgisini birleştir
            else:
                event.location = "Bilinmiyor"  # Coğrafi veri yoksa

            event.save()

            # Kullanıcıyı user_dashboard.html sayfasına yönlendir
            return redirect('user_dashboard')  # Tüm kullanıcılar için dashboard sayfasına yönlendir
    else:
        form = EventForm()

    return render(request, 'users/event_map.html', {'form': form})



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventForm
from .models import Event


@login_required
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

            # Kullanıcıya yönlendirme
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


def dashboard(request):
    # Kullanıcının oluşturduğu etkinlikler
    created_events = Event.objects.filter(created_by=request.user)

    # Kullanıcının katılabileceği etkinlikler (kendisi oluşturmadığı)
    available_events = Event.objects.exclude(created_by=request.user)

    # Kullanıcının oluşturduğu ve onaylanmış etkinlikler
    approved_events = Event.objects.filter(created_by=request.user, status='approved')

    # Kullanıcının katıldığı etkinlik sayısı
    user_events_count = request.user.events.count()  # Katıldığı etkinlikler

    # Kullanıcının oluşturduğu etkinlik sayısı
    user_created_events_count = created_events.count()  # Oluşturduğu etkinlikler

    # Onaylanmış etkinlikler (latitude ve longitude eksik olmayan)
    approved_events = Event.objects.filter(
        status='approved'
    ).exclude(
        latitude__isnull=True, longitude__isnull=True
    )

    # Harita için onaylanmış etkinliklerin verileri
    approved_event_data = [
        {
            'id': event.id,
            'name': event.name,
            'latitude': event.latitude,
            'longitude': event.longitude,
        }
        for event in approved_events
    ]

    # Kullanıcı puanını hesapla (eğer bir fonksiyon varsa)
    total_points = calculate_user_points(request.user)

    # Veriyi şablona gönder
    context = {
        'created_events': created_events,
        'available_events': available_events,
        'approved_events': approved_event_data,  # Harita için onaylı etkinlikler
        'user_events_count': user_events_count,
        'user_created_events_count': user_created_events_count,
        'total_points': total_points,
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


from django.db.models import Sum

def calculate_user_points(user):
    # Kullanıcının tüm Points'lerinden toplam puanı al
    total_points = user.user_points.aggregate(total=Sum('score'))['total'] or 0

    # Katıldığı etkinlik sayısını al
    joined_events_count = user.events.count()

    # Oluşturduğu onaylanmış etkinlik sayısını al
    created_events_count = user.created_events.filter(status='approved').count()

    return {
        'total_points': total_points,
        'joined_events_count': joined_events_count,
        'created_events_count': created_events_count,
    }

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



from .models import Event, Points

def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    # Kullanıcının zaten bu etkinliğe katılıp katılmadığını kontrol et
    if event in user.events.all():
        messages.warning(request, 'Bu etkinliğe zaten katıldınız!')
        return redirect('user_dashboard')  # Kullanıcıyı dashboard'a yönlendir

    # Kullanıcının katıldığı etkinliklerle çakışma kontrolü yap
    conflicting_events = Event.objects.filter(date=event.date, time=event.time).exclude(id=event.id)

    # Çakışan etkinlik var mı diye kontrol et
    for conflicting_event in conflicting_events:
        if conflicting_event in user.events.all():
            messages.warning(request, 'Bu etkinlik, daha önce katıldığınız bir etkinlik ile çakışmaktadır. Katılamazsınız.')
            return redirect('user_dashboard')  # Çakışma durumu varsa dashboard'a yönlendir

    # Etkinlik katılım işlemi
    user.events.add(event)

    # İlk etkinlik katılım bonusu
    first_join_bonus_exists = Points.objects.filter(user=user, point_type='first_join_bonus').exists()
    if not first_join_bonus_exists:
        add_points(user, 20, 'first_join_bonus')  # İlk katılım bonusu
        messages.success(request, 'İlk etkinliğinize katıldığınız için 20 puan kazandınız!')

    # Normal etkinlik katılım puanı ekle
    add_points(user, 10, 'join_event')  # Katılım puanı
    messages.success(request, f'{event.name} etkinliğine başarıyla katıldınız!')

    return redirect('user_dashboard')  # Katılım işlemi sonrası dashboard'a yönlendir



from django.shortcuts import render

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    messages = event.event_messages.all()  # Etkinlikle ilişkili mesajlar

    return render(request, 'users/event_detail.html', {
        'event': event,
        'messages': messages
    })

from django.http import HttpResponseRedirect

def send_message(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        message_text = request.POST['message']
        Message.objects.create(
            sender=request.user,  # Şu anki kullanıcı
            event=event,
            text=message_text
        )

        return HttpResponseRedirect(f'/event/{event.id}/')  # Yönlendirme



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Message

@login_required
def event_chat(request, event_id):
    # Etkinliği al
    event = get_object_or_404(Event, id=event_id)

    # Admin kullanıcısı değilse, etkinliğe katılımını kontrol et
    if not request.user.is_superuser:
        if event not in request.user.events.all():
            return redirect('user_dashboard')  # Katılmadığı etkinliğe erişmeye çalışıyorsa ana sayfaya yönlendir

    # Etkinliğe ait mesajları al
    messages = Message.objects.filter(event=event)

    # Mesaj gönderme işlemi
    if request.method == "POST":
        message_text = request.POST.get('message')
        if message_text:
            Message.objects.create(sender=request.user, event=event, text=message_text)

    return render(request, 'event_chat.html', {
        'event': event,
        'messages': messages,
    })


from django.contrib.auth.decorators import user_passes_test
from .forms import EventForm

# Sadece adminler için kontrol
def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_create_event(request):
    """
    Adminler için etkinlik oluşturma görünümü.
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Admin olarak etkinliği oluşturan
            event.save()
            return redirect('admin_dashboard')  # Admin dashboard'a yönlendirme
    else:
        form = EventForm()

    return render(request, 'admin_create_event.html', {'form': form})



from django.contrib.auth.decorators import login_required


@login_required
def admin_profile(request):
    if not request.user.is_staff:
        return redirect('home')  # Admin değilse ana sayfaya yönlendir

    user = get_object_or_404(User, id=3)  # id 3 olan kullanıcıyı bul
    points_data = calculate_user_points(user)  # Admin'in puan verileri

    return render(request, 'admin_profile.html', {  # 'users/admin_profile.html' kullanılıyor
        'user': user,
        'total_points': points_data['total_points'],
        'joined_events_count': points_data['joined_events_count'],
        'created_events_count': points_data['created_events_count'],
    })


@login_required
def delete_user(request, user_id):
    # Kullanıcıyı al
    user_to_delete = get_object_or_404(User, id=user_id)

    # Kullanıcının superuser (admin) olup olmadığını kontrol et
    if user_to_delete.is_superuser:
        messages.error(request, "Admin kullanıcı silinemez.")
        return redirect('admin_dashboard')

    # Kullanıcıyı sil
    user_to_delete.delete()

    # Admin paneline geri yönlendir
    return redirect('admin_dashboard')


def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Şifreyi şifreli olarak kaydediyoruz
            user.save()
            return redirect('admin_dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'create_user.html', {'form': form})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, Participant

