from django.contrib import admin
from .models import Warehouse, Box
from django.utils.html import format_html


class BoxInline(admin.TabularInline):
    model = Box
    extra = 1
    fields = ("number", "floor", "area", "price_per_month", "is_available")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "address", "temperature", "image_preview")
    search_fields = ("name", "address")
    inlines = [BoxInline]
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px;" />', obj.image.url
            )
        return "Нет фото"

    image_preview.short_description = "Превью изображения"
