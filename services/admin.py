from django.contrib import admin
from .models import Service, ServiceOrder


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price_per_unit",
        "unit_name",
    )
    list_filter = ("name", "description", "price_per_unit", "unit_name")
    search_fields = (
        "name",
        "description",
    )


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "service",
        "quantity",
        "start_date",
        "end_date",
        "promo_code",
        "created_at",
    )
    list_filter = (
        "user",
        "service",
        "quantity",
        "start_date",
        "end_date",
        "promo_code",
        "created_at",
    )
    search_fields = (
        "user__email",
        "service__name",
    )
