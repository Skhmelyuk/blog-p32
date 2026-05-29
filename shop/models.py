from django.db import models
from django.urls import reverse

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Назва товару")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="Слаг для URL")
    description = models.TextField(blank=True, verbose_name="Опис товару")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (грн)")
    image = models.ImageField(upload_to='product_images/%Y/%m/%d', blank=True, verbose_name="Зображення товару")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    is_active = models.BooleanField(default=True, verbose_name="Активний (доступний у магазині)")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товари"
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.name} ({self.price} грн)"

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.id, self.slug])

