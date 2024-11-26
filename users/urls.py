from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin giriş
    path('login/', views.login_view, name='user_login'),  # Kullanıcı girişi
    path('signup/', views.signup_view, name='signup'),  # Kayıt olma
    path('password_reset/', views.password_reset_view, name='password_reset'),  # Parola sıfırlama
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Kullanıcı dashboard
    path('logout/', views.logout_view, name='logout'),  # Çıkış yapma
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('user_login/', views.user_login, name='user_login'),

]
