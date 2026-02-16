from django.contrib import admin
from .models import Profile
from django.utils.html import format_html


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "avatar_preview")
    list_filter = ("user", "phone")
    search_fields = ("phone",)
    readonly_fields = ("avatar_preview",)

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-height: 200px;" />', obj.avatar.url
            )
        return "Нет фото"

    avatar_preview.short_description = "Превью аватара"
