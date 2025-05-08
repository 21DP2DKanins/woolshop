from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена, ₽"
    )
    image = models.ImageField(
        upload_to='products/%Y/%m/%d/', 
        blank=True, 
        null=True, 
        verbose_name="Изображение"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name