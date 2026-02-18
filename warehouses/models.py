from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название склада")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    image = models.ImageField(
        upload_to="warehouses/", blank=True, null=True, verbose_name="Изображение"
    )
    temperature = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="Температура"
    )
    ceiling_height = models.DecimalField(
        max_digits=3, decimal_places=1, verbose_name="Высота потолков"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    contacts = models.TextField(blank=True, verbose_name="Контакты")
    how_to_reach = models.TextField(blank=True, verbose_name="Как добраться")
    has_parking = models.BooleanField(default=False, verbose_name="Есть парковка")
    near_subway = models.BooleanField(default=False, verbose_name="Рядом с метро")
    rate_per_cubic_meter = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Ставка за м³ в месяц",
        default=0,
        help_text="Цена за 1 кубический метр в месяц",
    )

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"

    def __str__(self):
        return self.name


class Box(models.Model):
    SIZE_CATEGORIES = [
        ("small", "До 3 м²"),
        ("medium", "До 10 м²"),
        ("large", "От 10 м²"),
    ]
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, related_name="boxes", verbose_name="Склад"
    )
    number = models.CharField(max_length=20, verbose_name="Номер бокса")
    floor = models.PositiveSmallIntegerField(verbose_name="Этаж")
    area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Площадь")
    dimensions = models.CharField(max_length=50, verbose_name="Габариты")
    price_per_month = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name="Цена за месяц"
    )
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    size_category = models.CharField(
        max_length=10,
        choices=SIZE_CATEGORIES,
        blank=True,
        verbose_name="Категория размера",
    )
    length = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Длина (м)"
    )
    width = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Ширина (м)"
    )
    height = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name="Высота (м)"
    )

    class Meta:
        verbose_name = "Бокс"
        verbose_name_plural = "Боксы"

    def save(self, *args, **kwargs):
        volume = self.length * self.width * self.height
        if self.warehouse:
            self.price_per_month = volume * self.warehouse.rate_per_cubic_meter
        else:
            self.price_per_month = 0

        if self.area <= 3:
            self.size_category = "small"
        elif self.area <= 10:
            self.size_category = "medium"
        else:
            self.size_category = "large"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.warehouse.name} – бокс {self.number}"
