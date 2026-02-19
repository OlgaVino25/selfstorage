from django.contrib import admin
from .models import Warehouse, Box
from django.utils.html import format_html


class BoxInline(admin.TabularInline):
    model = Box
    extra = 1
    fields = (
        "number",
        "floor",
        "length",
        "width",
        "height",
        "area",
        "price_per_month",
        "is_available",
    )
    readonly_fields = ("price_per_month", "area")


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "temperature",
        "rate_per_cubic_meter",
        "image_preview",
    )
    search_fields = (
        "name",
        "address",
        "description",
    )
    inlines = [BoxInline]
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 200px;" />', obj.image.url
            )
        return "Нет фото"

    image_preview.short_description = "Превью изображения"
