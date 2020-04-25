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


