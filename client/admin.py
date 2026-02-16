from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "registration_date", "appointments_count")
    search_fields = ("name", "phone", "email")

    def appointments_count(self, obj):
        return obj.consultations.count()

    appointments_count.short_description = "Количество консультаций"
