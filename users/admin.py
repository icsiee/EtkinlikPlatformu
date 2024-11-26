from django.contrib import admin
from .models import User, Interest, Event, Participant, Message, Points


class UserAdmin(admin.ModelAdmin):
    # Kullanıcıları listelerken göstereceğimiz alanlar
    list_display = ('username', 'email', 'is_superuser', 'is_active', 'get_interests')

    # Kullanıcı adı, e-posta gibi alanlarda arama yapabilmek için
    search_fields = ('username', 'email')

    # Kullanıcının seçtiği ilgi alanlarını göstermek için özel bir method
    def get_interests(self, obj):
        # Kullanıcıya ait ilgi alanlarını birleştirip bir string olarak döndürüyoruz
        return ", ".join([interest.name for interest in obj.interests.all()])

    get_interests.short_description = 'İlgi Alanları'  # Admin panelinde gösterilecek başlık


# Interest modelini admin paneline ekleyelim
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)  # İlgi alanlarının adını gösteriyoruz
    search_fields = ('name',)  # İlgi alanı adında arama yapılabilmesi için


# Diğer modelleri admin paneline ekleyelim
admin.site.register(User, UserAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Event)
admin.site.register(Participant)
admin.site.register(Message)
admin.site.register(Points)