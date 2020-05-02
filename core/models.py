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


class Page(models.Model):
    PAGE_LINK = 'page_link'
    SIMPLE_LINK = 'simple_link'
    TYPES_CHOICES = (
        (PAGE_LINK, "Статическая страница"),
        (SIMPLE_LINK, "Обычная ссылка"),
    )
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    code = models.CharField(max_length=50, null=True,blank=True)
    type = models.CharField(max_length=50, choices=TYPES_CHOICES, default=SIMPLE_LINK)
    content = models.TextField(blank=True, null=True)
    position = models.PositiveIntegerField(default=1)
    is_menu_top = models.BooleanField("Показывать в верхнем меню",default=False)
    is_menu_footer = models.BooleanField("Показывать в нижнем меню",default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('position',)
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"
