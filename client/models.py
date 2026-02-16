from django.db import models
from django.db.models import Count
from datetime import date, timedelta
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinLengthValidator, RegexValidator, EmailValidator


class Client(models.Model):
    """Модель клиента"""

    phone = PhoneNumberField(
        unique=False,
        verbose_name="Телефон",
        region="RU",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Имя",
        validators=[
            MinLengthValidator(2, "Имя должно содержать минимум 2 символа"),
            RegexValidator(
                regex=r"^[а-яА-ЯёЁa-zA-Z\s\-]+$",
                message="Имя может содержать только буквы, пробелы и дефисы",
            ),
        ],
    )
    email = models.EmailField(
        blank=True, verbose_name="Email", validators=[EmailValidator()]
    )
    registration_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    def __str__(self):
        return f"{self.name} - {self.phone}"

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

