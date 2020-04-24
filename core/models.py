from django.db import models


class Carousel(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    img = models.ImageField(max_length=250,upload_to='carousel/')
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = 'Слайдер на главной'
        verbose_name_plural = 'Слайдер на главной'


