from django.contrib import admin
from .models import FAQCategory, FAQItem, Review
from django.utils.html import format_html
from django import forms
from tinymce.widgets import TinyMCE


class FAQItemAdminForm(forms.ModelForm):
    answer = forms.CharField(widget=TinyMCE(attrs={"cols": 80, "rows": 30}))

    class Meta:
        model = FAQItem
        fields = "__all__"


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    form = FAQItemAdminForm
    list_display = ("category", "question", "answer", "order")
    list_filter = ("category",)
    search_fields = (
        "question",
        "answer",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "author_name",
        "author_city",
        "photo_preview",
        "text",
        "full_review_link",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("author_name", "author_city", "text")
    readonly_fields = ("photo_preview",)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 200px;" />', obj.photo.url
            )
        return "Нет фото"

    photo_preview.short_description = "Превью фото"
