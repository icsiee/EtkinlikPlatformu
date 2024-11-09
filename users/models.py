from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

# Kullanıcı modeli
class User(AbstractUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    email = models.EmailField(unique=True)  # E-posta eşsiz olacak
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_admin = models.BooleanField(default=False)  # Yönetici yetkileri için

    def __str__(self):
        return self.username

# İlgi Alanları Modeli
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Her ilgi alanı eşsiz olacak
    description = models.TextField()

    def __str__(self):
        return self.name

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


# Katılımcı modeli
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"

# Mesaj modeli
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
