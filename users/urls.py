# users/urls.py

from django.urls import path
from . import views  # users uygulamasındaki views'i import ediyoruz

urlpatterns = [
    path('login/', views.login_view, name='login'),  # Giriş sayfası
    path('signup/', views.signup_view, name='signup'),  # Kayıt sayfası
    path('password_reset/', views.password_reset_view, name='password_reset'),  # Parola sıfırlama
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard yolu

]
