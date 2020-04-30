from django.db import models
from datetime import date, datetime
from django.utils import timezone
from django.core.exceptions import ImproperlyConfigured, ValidationError
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


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    advantages = models.TextField()
    disadvantages = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_show = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class ShockPriceProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    position = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['position']
        verbose_name = 'Успейте купить по шок-цене!'
        verbose_name_plural = 'Успейте купить по шок-цене!'


class ProductAttribute(models.Model):
    category = models.ManyToManyField('catalog.Category', through='catalog.ProductAttributeCategory',
                                      related_name='attributes')
    name = models.CharField('Название',max_length=128)
    code = models.SlugField(max_length=128)

    # Attribute types
    TEXT = "text"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    FLOAT = "float"
    DATE = "date"
    OPTION = "option"

    TYPE_CHOICES = (
        (TEXT, "Text"),
        (INTEGER,"Integer"),
        (BOOLEAN, "True / False"),
        (FLOAT, "Float"),
        (DATE, "Date"),
        (OPTION, "Option"),
    )
    type = models.CharField('Тип',choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],max_length=20)
    option_group = models.ForeignKey('catalog.ProductAttributeOptionGroup', blank=True, null=True,on_delete=models.CASCADE)
    required = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    CHECKBOX_LIST = 'checkbox_list'
    SELECT_LIST = 'select_list'
    SLIDER_INPUT = 'slider_input'
    WIDGET_TYPE_CHOICES = (
        (CHECKBOX_LIST, 'Чекбоксы'),
        (SELECT_LIST, 'Селектор'),
        (SLIDER_INPUT, 'Ползунок'),
    )
    widget_type_display = models.CharField(max_length=50, choices=WIDGET_TYPE_CHOICES,
                                           default=CHECKBOX_LIST)

    class Meta:
        ordering = ['display_order']
        verbose_name = 'Атрибут продукта'
        verbose_name_plural = 'Атрибуты продуктов'

    @property
    def is_option(self):
        return self.type == self.OPTION

    def __str__(self):
        return self.name

    def validate_value(self, value):
        validator = getattr(self, '_validate_{}'.format(self.type))
        validator(value)

    # Validators

    def _validate_text(self, value):
        if not isinstance(value, str):
            raise ValidationError("Must be str or unicode")

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise ValidationError("Must be a float")

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise ValidationError("Must be an integer")

    def _validate_date(self, value):
        if not (isinstance(value, datetime) or isinstance(value, date)):
            raise ValidationError(_("Must be a date or datetime"))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise ValidationError("Must be a boolean")


class ProductAttributeValue(models.Model):
    attribute = models.ForeignKey('catalog.ProductAttribute', verbose_name="Атрибут", on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', related_name='attribute_values',
                                verbose_name="Product",on_delete=models.CASCADE)
    value_text = models.TextField('Текст', blank=True, null=True)
    value_integer = models.IntegerField('Integer', blank=True, null=True)
    value_boolean = models.NullBooleanField('Boolean', blank=True)
    value_float = models.FloatField('Float', blank=True, null=True)
    value_date = models.DateField('Date', blank=True, null=True)
    value_option = models.ForeignKey('catalog.ProductAttributeOption', blank=True, null=True,
                                     verbose_name="Value option",on_delete=models.CASCADE)

    def _get_value(self):
        return getattr(self, 'value_{}'.format(self.attribute.type))

    def _set_value(self, new_value):
        if self.attribute.is_option and isinstance(new_value, str):
            # Need to look up instance of AttributeOption
            new_value = self.attribute.option_group.options.get(
                option=new_value)
        setattr(self, 'value_{}'.format(self.attribute.type), new_value)

    value = property(_get_value, _set_value)

    class Meta:
        unique_together = ('attribute', 'product')
        verbose_name = 'Значение атрибута продукта'
        verbose_name_plural = 'Значения атрибутов продуктов'

    def __str__(self):
        return self.summary()

    def summary(self):
        return "{}: {}".format(self.attribute.name, self.value_as_text)

    @property
    def value_as_text(self):
        property_name = '_{}_as_text'.format(self.attribute.type)
        return getattr(self, property_name, self.value)

    @property
    def _entity_as_text(self):
        return str(self.value)


class ProductAttributeCategory(models.Model):
    attribute = models.ForeignKey('catalog.ProductAttribute',on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return '{}-{}'.format(self.attribute.name, self.category.name)

    class Meta:
        ordering = ['attribute', 'category']
        unique_together = ('attribute', 'category')
        verbose_name = 'Атрибуты/Категории'
        verbose_name_plural = 'Атрибуты/Категории'


class ProductAttributeOptionGroup(models.Model):
    name = models.CharField(max_length=128, null=True, blank=True)
    code = models.SlugField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа параметров атрибута'
        verbose_name_plural = 'Группа параметров атрибута'

    @property
    def option_summary(self):
        options = [o.option for o in self.options.all()]
        return ", ".join(options)

    @property
    def color_options(self):
        return self.options.order_by('option')

    @property
    def default_options_order(self):
        return self.options.order_by('option')

    @property
    def size_options_order(self):
        return self.options.order_by('minimum')


class ProductAttributeOption(models.Model):
    group = models.ForeignKey('catalog.ProductAttributeOptionGroup', related_name='options',on_delete=models.CASCADE)
    option = models.CharField(max_length=255)
    show_value = models.CharField(max_length=255, null=True, blank=True)
    display_order = models.PositiveIntegerField('Позиция', default=0)

    def __str__(self):
        return self.option

    class Meta:
        ordering = ('option',)
        unique_together = ('group', 'option')
        verbose_name = 'Опция атрибута'
        verbose_name_plural = 'Опции для атрибутов'


