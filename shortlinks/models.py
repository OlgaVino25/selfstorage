from django.db import models


class ShortLink(models.Model):
    slug = models.SlugField(
        unique=True,
        verbose_name="Короткий код",
    )
    target_url = models.URLField(
        verbose_name="Ссылка",
    )
    clicks = models.PositiveIntegerField(
        default=0,
        verbose_name="Клики",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    description = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Описание",
    )

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"

    def __str__(self):
        return self.slug
