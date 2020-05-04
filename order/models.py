from decimal import Decimal as D
from django.db import models
from django.conf import settings


class ShippingAddress(models.Model):
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Адрес доставки'
        verbose_name_plural = 'Адреса доставки'


class Order(models.Model):
    number = models.CharField(max_length=128, db_index=True, unique=True)
    basket = models.ForeignKey(
        'basket.Basket',null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders',
                             null=True, blank=True, on_delete=models.SET_NULL)

    total_excl_tax = models.DecimalField(decimal_places=2, max_digits=12)
    shipping_excl_tax = models.DecimalField(decimal_places=2, max_digits=12,default=0)

    shipping_address = models.ForeignKey(
        'order.ShippingAddress', null=True, blank=True, on_delete=models.SET_NULL)
    shipping_method = models.CharField(max_length=128, blank=True)

    status = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)
    date_placed = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ['-date_placed']
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return "#{}".format(self.number)

    @property
    def num_lines(self):
        return self.lines.count()

    @property
    def num_items(self):
        num_items = 0
        for line in self.lines.all():
            num_items += line.quantity
        return num_items

    @property
    def total_sum_lines(self):
        total = D('0.00')
        for line in self.lines.all():
            total += line.total_line_price
        return total


class Line(models.Model):
    order = models.ForeignKey('order.Order', related_name='lines', on_delete=models.CASCADE)
    product = models.ForeignKey(
        'catalog.Product', on_delete=models.SET_NULL, blank=True, null=True)

    quantity = models.PositiveIntegerField(default=1)
    line_price_excl_tax = models.DecimalField(decimal_places=2, max_digits=12)

    # Retail price at time of purchase
    unit_retail_price = models.DecimalField(decimal_places=2, max_digits=12,
        blank=True, null=True)

    class Meta:
        ordering = ['pk']
        verbose_name = "Строка заказа"
        verbose_name_plural = "Строки заказа"

    def __str__(self):
        return str(self.pk)

    @property
    def total_line_price(self):
        return self.line_price_excl_tax * self.quantity
