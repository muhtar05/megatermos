from django.db import models


class Carousel(models.Model):
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(max_length=250,upload_to='carousel/')
    position = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('position',)
        verbose_name = 'Слайдер на главной'
        verbose_name_plural = 'Слайдер на главной'


class Settings(models.Model):
    mode_of_operation = models.CharField("Режим работы",max_length=255, blank=True, null=True)
    phone = models.CharField("Телефон",max_length=255, blank=True, null=True)
    slogan = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return 'Настройки'

    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"


class Menu(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'


class Page(models.Model):
    content = models.TextField()
    menu = models.ForeignKey(Menu,null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"


