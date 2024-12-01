from django.urls import path, include
from . import views
from django.contrib import admin
from .views import user_detail
from .views import admin_dashboard, admin_profile  # admin_profile view'ını doğru şekilde import edin


urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),  # Admin giriş
    path('login/', views.login_view, name='user_login'),  # Kullanıcı girişi
    path('signup/', views.signup_view, name='signup'),  # Kayıt olma
    path('password_reset/', views.password_reset_view, name='password_reset'),  # Parola sıfırlama
    path('dashboard/', views.user_dashboard, name='user_dashboard'),  # Kullanıcı dashboard
    path('logout/', views.logout_view, name='logout'),  # Çıkış yapma
    path('user_login/', views.user_login, name='user_login'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('events/', views.event_list, name='event_list'),  # Bu URL ile etkinlikler listelenir
    path('event/create/', views.create_event, name='create_event'),
    path('dashboard/event/create/', views.create_event, name='create_event'),
    path('admin/events/', views.event_list, name='event_list'),

    path('admin/', admin.site.urls),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),  # Etkinlik düzenleme
    path('join_event/<int:event_id>/', views.join_event, name='join_event'),
    path('event/approve/<int:event_id>/', views.approve_event, name='approve_event'),
    path('event/reject/<int:event_id>/', views.reject_event, name='reject_event'),
    path('event/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # Etkinlik detay URL'si
    path('event/<int:event_id>/edit/', views.update_event, name='update_event'),  # Etkinlik düzenleme URL'si
    path('event/map/', views.user_event_map, name='create_event'),  # Yeni etkinlik oluşturma
    path('event/map/<int:event_id>/', views.user_event_map, name='edit_event'),  # Etkinlik düzenleme
    path('user/<int:user_id>/', user_detail, name='user_detail'),
    path('interests/', views.user_interests, name='user_interests'),  # İlgi alanlarını listele
    path('add_interest/', views.add_interest, name='add_interest'),  # Yeni ilgi alanı ekle
    path('interest/<int:interest_id>/delete/', views.delete_interest, name='delete_interest'),
    path('interest/<int:interest_id>/edit/', views.edit_interest, name='edit_interest'),
    path('event/<int:event_id>/resubmit/', views.resubmit_event, name='resubmit_event'),
    path('dashboard/rejected-events/', views.rejected_events, name='rejected_events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/chat/', views.event_chat, name='event_chat'),
    path('dashboard/admin/profile/', admin_profile, name='admin_profile'),  # Admin profil sayfası için doğru URL
    path('dashboard/admin/dashboard/', admin_dashboard, name='admin_dashboard'),  # Admin paneli için doğru URL
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('create_user/', views.create_user, name='create_user'),
    # Admin için etkinlik oluşturma
    path('dashboard/admin/create-event/', views.admin_create_event, name='admin_create_event'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('leave_event/<int:event_id>/', views.leave_event, name='leave_event'),

    # Etkinlik listesi
    # Diğer URL'ler...
    # Other paths for logout, etc.
]