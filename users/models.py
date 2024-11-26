from django.contrib.auth.models import AbstractUser
from django.db import models


# İlgi Alanları Modeli
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Her ilgi alanı eşsiz olacak
    description = models.TextField()

    def __str__(self):
        return self.name


# Kullanıcı Modeli
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Özel User Manager
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

# Kullanıcı Modeli
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
    email = models.EmailField(unique=True)  # E-posta eşsiz olacak
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_admin = models.BooleanField(default=False)  # Yönetici yetkileri için
    interests = models.ManyToManyField('Interest', blank=True)  # Many-to-many ilişki

    # related_name parametrelerini ekliyoruz
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    # Kullanıcı modeline UserManager'ı bağlıyoruz
    objects = UserManager()

    def __str__(self):
        return self.username


# Etkinlik Modeli
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


# Katılımcı Modeli
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"


# Mesaj Modeli
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_messages')
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.event.name}"


# Puan Sistemi Modeli
class Points(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    score = models.PositiveIntegerField()
    date_earned = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.score} points"
