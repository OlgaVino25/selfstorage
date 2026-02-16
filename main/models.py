from django.db import models


class FAQCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    category = models.ForeignKey(
        FAQCategory,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Категория",
    )
    question = models.CharField(max_length=255, verbose_name="Вопрос")
    answer = models.TextField(verbose_name="Ответ")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Элемент FAQ"
        verbose_name_plural = "Элементы FAQ"
        ordering = ["order"]

    def __str__(self):
        return self.question


class Review(models.Model):
    author_name = models.CharField(max_length=100, verbose_name="Имя автора")
    author_city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    photo = models.ImageField(
        upload_to="reviews/", blank=True, null=True, verbose_name="Фото"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    full_review_link = models.URLField(
        blank=True, verbose_name="Ссылка на полный отзыв"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.author_name}"
