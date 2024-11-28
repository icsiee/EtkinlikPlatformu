from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin giriş
    path('login/', views.login_view, name='user_login'),  # Kullanıcı girişi
    path('signup/', views.signup_view, name='signup'),  # Kayıt olma
    path('password_reset/', views.password_reset_view, name='password_reset'),  # Parola sıfırlama
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Kullanıcı dashboard
    path('logout/', views.logout_view, name='logout'),  # Çıkış yapma
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard
    path('user_login/', views.user_login, name='user_login'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/event/list/', views.event_list, name='event_list'),
    path('events/add/', views.event_add, name='event_add'),
    path('events/edit/<int:pk>/', views.event_edit, name='event_edit'),
    path('events/delete/<int:pk>/', views.event_delete, name='event_delete'),
    path('create/', views.create_event, name='create_event'),
    path('dashboard/event/create/', views.create_event, name='create_event'),
    path('admin/', admin.site.urls),

    # Other paths for logout, etc.
]