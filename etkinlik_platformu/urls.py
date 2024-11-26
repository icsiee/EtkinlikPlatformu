# etkinlik_platformu/etkinlik_platformu/urls.py

from django.contrib import admin
from django.urls import path, include  # 'include' import edilmelidir
from users import views  # users uygulamasındaki views'i import ediyoruz

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneline erişim
    path('users/', include('users.urls')),  # 'users' uygulamasının URL'lerini dahil et
    path('', views.login_view, name='login'),  # Ana sayfa olarak login ekranına yönlendirme
    path('', include('users.urls')),  # users uygulamasındaki URL'leri dahil et
    path('dashboard/', include('users.urls')),
]
