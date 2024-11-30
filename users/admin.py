from django.contrib import admin
from .models import User, Interest, Event, Participant, Message, Points

try:
    admin.site.unregister(Interest)
except admin.sites.NotRegistered:
    pass  # The model is not registered, so no action needed


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'surname', 'get_interests')  # 'get_interests' fonksiyonu

    def get_interests(self, obj):
        # Kullanıcının ilgi alanlarını döndüren metod
        return ", ".join([interest.name for interest in obj.interests.all()])
    get_interests.short_description = 'İlgi Alanları'

class InterestAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # İlgi alanlarının adı ve açıklaması listelenecek
    search_fields = ('name',)  # İlgi alanı adına göre arama yapabilme
    list_filter = ('name',)  # İlgi alanlarına göre filtreleme
    ordering = ('name',)  # İlgi alanlarını isme göre sıralama

# Register other models
admin.site.register(User, UserAdmin)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Message)
admin.site.register(Points)
