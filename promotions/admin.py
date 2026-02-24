from django.contrib import admin

from .models import PromoCode, ShortcutLink
from .shortio import create_short_link, get_clicks


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_percent", "valid_from", "valid_to")
    list_filter = ("code", "discount_percent", "valid_from", "valid_to")
    search_fields = ("code",)


@admin.register(ShortcutLink)
class ShortcutLinkAdmin(admin.ModelAdmin):
    """Интерфейс ShortcutLink."""

    list_display = ('name', 'target_url', 'short_url', 'clicks', 'created_at')
    actions = ('generate_short_link', 'update_clicks')

    def generate_short_link(self, request, queryset):
        """Генерация короткой ссылки."""

        for obj in queryset:
            if not obj.short_url:
                obj.short_url = create_short_link(obj.target_url)
                obj.save(update_fields=['short_url'])

    generate_short_link.short_description = 'Сгенерировать ссылку'

    def update_clicks(self, request, queryset):
        """Обеновление статичтики."""

        for obj in queryset:
            if obj.short_url:
                obj.clicks = get_clicks(obj.target_url)
                obj.save(update_fields=['clicks'])

    update_clicks.short_description = 'Обновить клики'
