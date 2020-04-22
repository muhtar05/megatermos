from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    parent = TreeForeignKey('self', blank=True, null=True,
                            related_name='children', db_index=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    artikul = models.CharField(max_length=255, null=True, blank=True)
    price_opt = models.DecimalField('Оптовая Цена', decimal_places=2, max_digits=12, blank=True, null=True)
    price = models.DecimalField('Цена', decimal_places=2, max_digits=12, blank=True, null=True)
    old_price = models.DecimalField('Старая Цена', decimal_places=2, max_digits=12, blank=True, null=True)
    img = models.ImageField(max_length=250,upload_to='products/')
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def image_tag(self):
        from django.utils.html import mark_safe
        if self.img:
            return mark_safe('<img src="{}" width="100px" height="100px" />'.format(self.img.url))
        else:
            return ''

    image_tag.short_description = 'Image'




