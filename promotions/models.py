from django.db import models
from django.utils import timezone


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Код промокода")
    discount_percent = models.PositiveSmallIntegerField(
        verbose_name="Скидка", help_text="Скидка в %"
    )
    valid_from = models.DateTimeField(verbose_name="Действует с")
    valid_to = models.DateTimeField(verbose_name="Действует до")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.valid_from <= now <= self.valid_to

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"
