from django.contrib import admin
from .models import User, Event, Participant, Message, Points, Interest  # Modelleri import edin

# User modelini admin paneline ekleyin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

# Interest modelini admin paneline ekleyin
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Hangi alanları göstereceğiniz
    search_fields = ('name',)

# Event modelini admin paneline ekleyin
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'created_by')
    search_fields = ('name', 'location')

# Participant modelini admin paneline ekleyin
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'join_date')
    search_fields = ('user__username', 'event__name')

# Message modelini admin paneline ekleyin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'event', 'sent_at')
    search_fields = ('sender__username', 'event__name')

# Points modelini admin paneline ekleyin
class PointsAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'date_earned')
    search_fields = ('user__username',)

# Admin Paneline Modelleri Kaydedin
admin.site.register(User, UserAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Points, PointsAdmin)
