from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# İlgi Alanları Modeli
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # description isteğe bağlı

    def __str__(self):
        return self.name

# Kullanıcı Modeli
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if password:
            user.set_password(password)  # Parola şifrelenerek kaydedilir
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    points = models.ManyToManyField('Points', related_name='users', blank=True)

    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[('K', 'Kadın'), ('E', 'Erkek')],
        null=True,
        blank=True,
    )
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_admin = models.BooleanField(default=False)  # Bu alanı kaldırabilirsiniz.
    interests = models.ManyToManyField('Interest', blank=True)
    events = models.ManyToManyField('Event', through='Participant', related_name='participants')

    objects = UserManager()

    def __str__(self):
        return self.username

# Etkinlik Modeli
class Event(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Müzik'),
        ('sports', 'Spor'),
        ('education', 'Eğitim'),
        ('technology', 'Teknoloji'),
        ('art', 'Sanat'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Onay Bekliyor'),
        ('approved', 'Onaylanmış'),
        ('rejected', 'Reddedilmiş'),
    ]

    name = models.CharField(max_length=100)  # Etkinlik adı
    description = models.TextField()  # Etkinlik açıklaması
    date = models.DateField()  # Etkinlik tarihi
    time = models.TimeField(null=True, blank=True)  # Etkinlik saati
    duration = models.DurationField(null=True, blank=True)  # Etkinlik süresi
    location = models.CharField(max_length=100)  # Etkinlik yeri
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,  # Kategori seçenekleri
        default='music'  # Varsayılan değer
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')  # Düzenlendi
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'  # Varsayılan değer "Onay Bekliyor"
    )

    def __str__(self):
        return self.name

# Katılımcı Modeli
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.event.name}'

# Mesaj Modeli
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # Mesajı gönderen kullanıcı
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_messages')  # Etkinlik
    text = models.TextField()  # Mesaj içeriği
    sent_at = models.DateTimeField(auto_now_add=True)  # Gönderilme zamanı

    def __str__(self):
        return f"Message from {self.sender.username} in {self.event.name}"

# Puan Sistemi Modeli
from django.conf import settings

class Points(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_points')  # related_name değiştirilmiştir
    score = models.IntegerField()
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.score} points'


class Event(models.Model):
    name = models.CharField(max_length=255)  # Etkinlik adı
    description = models.TextField()  # Etkinlik açıklaması
    duration = models.IntegerField()  # Süre (örneğin dakika olarak)
    category = models.CharField(
        max_length=50,
        choices=[
            ('conference', 'Conference'),
            ('workshop', 'Workshop'),
            ('seminar', 'Seminar'),
        ]
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Enlem
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)  # Boylam
    location = models.CharField(max_length=255, null=True, blank=True)  # Konum bilgisi

    def __str__(self):
        return self.name


class Message(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"