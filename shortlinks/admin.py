from django.contrib import admin
from django.utils.html import format_html
from .models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ("slug", "target_url", "short_url_display", "clicks", "created_at")
    search_fields = ("slug",)
    list_filter = ("created_at",)

    def short_url_display(self, obj):
        request = getattr(self, "request", None)
        if request:
            protocol = "https" if request.is_secure() else "http"
            domain = request.get_host()
            short_url = f"{protocol}://{domain}/go/{obj.slug}/"
            return format_html(
                '<a href="{}" target="_blank">{}</a>', short_url, short_url
            )
        return f"/go/{obj.slug}/"

    short_url_display.short_description = "Короткая ссылка"

    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)
