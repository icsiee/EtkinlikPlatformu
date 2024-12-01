from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings

# İlgi Alanları Modeli
class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  # İsteğe bağlı açıklama

    def __str__(self):
        return self.name

# Kullanıcı Yönetim Modeli
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email alanı zorunludur.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Şifrelenmiş şekilde kaydedilir
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
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    interests = models.ManyToManyField('Interest', blank=True)
    points = models.ManyToManyField('Points', related_name='users', blank=True)
    events = models.ManyToManyField(
        'Event', through='Participant', related_name='participants', blank=True
    )

    objects = UserManager()

    # Kullanıcının toplam puanını hesaplayacak fonksiyon
    def total_points(self):
        return sum(point.value for point in self.points.all())  # Puanların toplamını döndürür
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
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='created_events'
    )
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
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages'
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='event_messages'
    )
    text = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} in {self.event.name}"

# Puan Sistemi Modeli
class Points(models.Model):
    POINT_TYPE_CHOICES = [
        ('join_event', 'Etkinliğe Katılım'),
        ('create_event', 'Etkinlik Oluşturma'),
        ('first_join_bonus', 'İlk Katılım Bonusu'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_points'
    )
    score = models.IntegerField()
    point_type = models.CharField(
        max_length=20, choices=POINT_TYPE_CHOICES, default='join_event'
    )
    date_awarded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.score} points ({self.point_type})'
