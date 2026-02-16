from django.db import models
from django.conf import settings
from promotions.models import PromoCode


class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    price_per_unit = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Цена за единицу"
    )
    unit_name = models.CharField(
        max_length=50, default="стеллаж", verbose_name="Единица измерения"
    )

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name


class ServiceOrder(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="service_orders",
        verbose_name="Пользователь",
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name="orders", verbose_name="Услуга"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    promo_code = models.ForeignKey(
        PromoCode,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="service_orders",
        verbose_name="Промокод",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ услуги"
        verbose_name_plural = "Заказы услуг"

    def __str__(self):
        return f"{self.user.email} – {self.service.name} x{self.quantity}"
