from django.contrib import admin
from .models import Rent, StoredItem


class StoredItemInline(admin.TabularInline):
    model = StoredItem
    extra = 1
    fields = ("name", "description", "quantity", "category")


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    inlines = [StoredItemInline]
    list_display = (
        "get_user_first_name",
        "get_user_last_name",
        "get_user_phone",
        "get_user_email",
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
        "user__first_name",
        "user__last_name",
        "user__profile__phone",
        "user__profile__address",
        "box__number",
        "box__warehouse__name",
    )
    readonly_fields = ("total_price",)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user__profile")

    def get_user_email(self, obj):
        return obj.user.email

    get_user_email.short_description = "Email"
    get_user_email.admin_order_field = "user__email"

    def get_user_first_name(self, obj):
        return obj.user.first_name

    get_user_first_name.short_description = "Имя"
    get_user_first_name.admin_order_field = "user__first_name"

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = "Фамилия"
    get_user_last_name.admin_order_field = "user__last_name"

    def get_user_phone(self, obj):
        if hasattr(obj.user, "profile"):
            return obj.user.profile.phone
        return ""

    get_user_phone.short_description = "Телефон"
    get_user_phone.admin_order_field = "user__profile__phone"

    def get_user_address(self, obj):
        if hasattr(obj.user, "profile"):
            return obj.user.profile.address
        return ""

    get_user_address.short_description = "Адрес"
    get_user_address.admin_order_field = "user__profile__address"
