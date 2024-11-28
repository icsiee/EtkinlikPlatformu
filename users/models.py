from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# İlgi Alanları Modeli
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

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
    is_admin = models.BooleanField(default=False)
    interests = models.ManyToManyField('Interest', blank=True)

    objects = UserManager()

    def __str__(self):
        return self.username

# Etkinlik Modeli
from django.db import models
from users.models import User  # Kullanıcı modeli için

class Event(models.Model):
    name = models.CharField(max_length=100)  # Etkinlik adı
    description = models.TextField()  # Etkinlik açıklaması
    date = models.DateField()  # Etkinlik tarihi
    time = models.TimeField(null=True, blank=True)  # Etkinlik saati
    duration = models.DurationField(null=True, blank=True)  # Etkinlik süresi
    location = models.CharField(max_length=100)  # Etkinlik yeri
    category = models.CharField(max_length=50)  # Etkinlik kategorisi
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')

    def __str__(self):
        return self.name

# Katılımcı Modeli
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')  # Kullanıcı
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')  # Etkinlik
    join_date = models.DateTimeField(auto_now_add=True)  # Katılım tarihi

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

# Mesaj Modeli
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')  # Mesajı gönderen kullanıcı
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_messages')  # Etkinlik
    text = models.TextField()  # Mesaj içeriği
    sent_at = models.DateTimeField(auto_now_add=True)  # Gönderilme zamanı

    def __str__(self):
        return f"Message from {self.sender.username} in {self.event.title}"

# Puan Sistemi Modeli
class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')  # Kullanıcı
    score = models.PositiveIntegerField()  # Puan
    date_earned = models.DateTimeField(auto_now_add=True)  # Puan kazanılma tarihi

    def __str__(self):
        return f"{self.user.username}: {self.score} points"
