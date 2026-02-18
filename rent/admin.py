from django.contrib import admin
from .models import Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "box",
        "start_date",
        "end_date",
        "deposit",
        "promo_code",
        "total_price",
        "is_active",
        "created_at",
    )
    list_filter = (
        "start_date",
        "end_date",
        "deposit",
        "promo_code",
        "is_active",
        "created_at",
    )
    search_fields = (
        "user__email",
        "box__number",
        "box__warehouse__name",
    )
    readonly_fields = ("total_price",)
