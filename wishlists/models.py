from django.db import models
from django.conf import settings


class WishList(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='wishlists',null=True,on_delete=models.CASCADE)
    hash_id = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return str(self.pk)

    def is_allowed_to_edit(self, user):
        return user == self.owner

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"

    def add(self, product):
        lines = self.lines.filter(product=product)
        if len(lines) == 0:
            self.lines.create(
                product=product, title=product.get_title())
        # else:
        #     line = lines[0]
        #     line.quantity += 1
        #     line.save()


class Line(models.Model):
    wishlist = models.ForeignKey('wishlists.WishList', related_name='lines',on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product',related_name='wishlists_lines', on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField( default=1)
    title = models.CharField(max_length=255)

    def __str__(self):
        return '{}x {}'.format(self.quantity, self.title)

    def get_title(self):
        if self.product:
            return self.product.get_title()
        else:
            return self.title

    class Meta:
        ordering = ['pk']
        unique_together = (('wishlist', 'product'),)
        verbose_name = "Строка Избранное"
        verbose_name_plural = "Строки Избранное"



