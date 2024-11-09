# users/urls.py

from . import views  # users uygulamasındaki views'i import ediyoruz
from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('login/', views.login_view, name='login'),  # Giriş sayfası
    path('signup/', views.signup_view, name='signup'),  # Kayıt sayfası
    path('password_reset/', views.password_reset_view, name='password_reset'),  # Parola sıfırlama
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Kullanıcı arayüzü
    path('logout/', views.logout_view, name='logout'),  # Çıkış yapma URL'si

]
