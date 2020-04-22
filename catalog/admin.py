from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from catalog.models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','image_tag','price_opt','price','old_price')
    list_filter = ('category',)


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product, ProductAdmin)


