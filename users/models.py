from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

# Kullanıcı modeli
class User(AbstractUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    interests = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_admin = models.BooleanField(default=False)  # Yönetici yetkileri için

    def __str__(self):
        return self.username


# Etkinlik modeli
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')

    def __str__(self):
        return self.name


# Katılımcı modeli (bir kullanıcının hangi etkinliklere katıldığını izlemek için)
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


# Mesaj modeli (her etkinlik için mesajlaşma sistemi)
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_messages')
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.event.name}"


# Puan sistemi
class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    score = models.PositiveIntegerField()
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.score} points"


User = get_user_model()

# Admin kullanıcı ekleme fonksiyonu
def create_admin():
    try:
        admin_user, created = User.objects.get_or_create(
            username='admin',  # Sabit kullanıcı adı
            defaults={
                'is_superuser': True,
                'is_staff': True,
                'is_admin': True,
                'email': 'admin@example.com',
            }
        )
        if created:
            admin_user.set_password('admin')  # Sabit parola
            admin_user.save()
            print("Admin kullanıcı başarıyla oluşturuldu.")
        else:
            print("Admin kullanıcı zaten mevcut.")
    except IntegrityError:
        print("Admin kullanıcı oluşturulurken bir hata oluştu.")


# Bu fonksiyonu Django yönetici komutları ile tetikleyebilirsiniz.