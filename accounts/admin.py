from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"
    fields = ("phone", "address", "avatar")


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "first_name",
        "last_name",
        "get_phone",
        "get_address",
        "email",
        "is_staff",
    )

    def get_phone(self, obj):
        return obj.profile.phone if hasattr(obj, "profile") else ""

    get_phone.short_description = "Телефон"

    def get_address(self, obj):
        return obj.profile.address if hasattr(obj, "profile") else ""

    get_address.short_description = "Адрес"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("profile")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
