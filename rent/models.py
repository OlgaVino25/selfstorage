from django.db import models
from django.conf import settings
from decimal import Decimal
from warehouses.models import Box
from promotions.models import PromoCode


class Rent(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rents",
        verbose_name="Пользователь",
    )
    box = models.ForeignKey(
        Box, on_delete=models.PROTECT, related_name="rents", verbose_name="Бокс"
    )
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    deposit = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Депозит"
    )
    promo_code = models.ForeignKey(
        PromoCode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="rents",
        verbose_name="Промокод",
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Итоговая стоимость",
        blank=True,
        null=True,
    )
    delivery_required = models.BooleanField(
        default=False, verbose_name="Требуется доставка"
    )
    measurements_required = models.BooleanField(
        default=False, verbose_name="Требуются замеры"
    )

    class Meta:
        verbose_name = "Аренда"
        verbose_name_plural = "Аренды"
        ordering = ["-start_date"]

    def save(self, *args, **kwargs):
        base_price = self.box.price_per_month
        months = (self.end_date.year - self.start_date.year) * 12 + (
            self.end_date.month - self.start_date.month
        )
        if months <= 0:
            months = 1
        total = base_price * months
        if self.promo_code and self.promo_code.is_valid():
            discount = Decimal(self.promo_code.discount_percent) / Decimal(100)
            total = total * (Decimal(1) - discount)
        self.total_price = total
        super().save(*args, **kwargs)


class StoredItem(models.Model):
    CATEGORY_CHOICES = [
        ("seasonal", "Сезонные вещи"),
        ("other", "Другое"),
    ]
    rent = models.ForeignKey(
        "Rent", on_delete=models.CASCADE, related_name="items", verbose_name="Аренда"
    )
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other",
        verbose_name="Категория",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Хранимая вещь"
        verbose_name_plural = "Хранимые вещи"

    def __str__(self):
        return f"{self.name} (x{self.quantity})"
