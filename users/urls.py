from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin giriş
    path('login/', views.login_view, name='login'),  # login URL'ini tanımlayın
    path('signup/', views.signup_view, name='signup'),  # Kayıt olma
    path('password_reset/', views.password_reset_view, name='password_reset'),  # Parola sıfırlama
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Kullanıcı dashboard
    path('logout/', views.logout_view, name='logout'),  # Çıkış yapma
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('home/', views.home_view, name='home'),  # Ana sayfa yönlendirme için
    path('login/', views.login_view, name='user_login'),  # Burada 'user_login' adını kullanın

]
