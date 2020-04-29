from decimal import Decimal as D
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.db import models
from django.conf import settings


class OpenBasketManager(models.Manager):
    status_filter = "Open"

    def get_queryset(self):
        return super().get_queryset().filter(
            status=self.status_filter)

    def get_or_create(self, **kwargs):
        return self.get_queryset().get_or_create(
            status=self.status_filter, **kwargs)


class Basket(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='baskets',
                              null=True, on_delete=models.CASCADE)
    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN,"Open - currently active"),
        (MERGED,"Merged - superceded by another basket"),
        (SAVED, "Saved - for items to be purchased later"),
        (FROZEN, "Frozen - the basket cannot be modified"),
        (SUBMITTED, "Submitted - has been ordered at the checkout"),
    )
    status = models.CharField(max_length=128, default=OPEN, choices=STATUS_CHOICES)
    date_created = models.DateTimeField(auto_now_add=True)
    date_merged = models.DateTimeField(null=True, blank=True)
    date_submitted = models.DateTimeField(null=True,blank=True)

    editable_statuses = (OPEN, SAVED)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return str(self.pk)

    objects = models.Manager()
    open = OpenBasketManager()

    def add_product(self, product, quantity=1):
        if not self.id:
            self.save()

        defaults = {
            'quantity': quantity,
            'price_excl_tax': product.price,
        }

        line, created = self.lines.get_or_create(
            line_reference=str(product.pk),
            product=product,
            defaults=defaults)
        if created:
            pass
        else:
            line.quantity = max(0, line.quantity + quantity)
            line.save()

        return line, created

    @property
    def can_be_edited(self):
        return self.status in self.editable_statuses

    @property
    def num_lines(self):
        return self.all_lines().count()

    @property
    def num_items(self):
        return sum(line.quantity for line in self.lines.all())

    @property
    def get_total_sum(self):
        total = D('0.00')
        for l in self.lines.all():
            total += l.price_excl_tax
        return total


class Line(models.Model):
    basket = models.ForeignKey('basket.Basket',on_delete=models.CASCADE,related_name='lines')
    line_reference = models.SlugField("Line Reference", max_length=128, db_index=True)
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE,
                                related_name='basket_lines', verbose_name="Product")

    quantity = models.PositiveIntegerField(default=1)
    price_excl_tax = models.DecimalField(decimal_places=2, max_digits=12,null=True)

    # Track date of first addition
    date_created = models.DateTimeField(auto_now_add=True, db_index=True)
    date_updated = models.DateTimeField(auto_now=True, db_index=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._discount_excl_tax = D('0.00')
        self._discount_incl_tax = D('0.00')

    class Meta:
        ordering = ['date_created', 'pk']
        unique_together = ("basket", "line_reference")
        verbose_name = 'Строка корзины'
        verbose_name_plural = 'Строки корзины'

    def __str__(self):
        return "Basket {}, Product {}, quantity {}".format(self.basket.pk, self.product.pk,self.quantity)

    def save(self, *args, **kwargs):
        if not self.basket.can_be_edited:
            raise PermissionDenied("You cannot modify a {} basket".format(self.basket.status.lower()))
        return super().save(*args, **kwargs)

    @property
    def line_price_excl_tax(self):
        return self.quantity * self.price_excl_tax
