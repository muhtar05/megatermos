from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from catalog.models import (Category, Product, ProductAttributeOption,
                            ProductAttributeOptionGroup,ProductAttribute,ProductAttributeCategory,ProductAttributeValue,)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','image_tag','price_opt','price','old_price')
    list_filter = ('category',)


class ProductAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type')
    prepopulated_fields = {"code": ("name", )}


class ProductAttributeCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'attribute', )
    list_filter = ('category', 'attribute')


class ProductAttributeValueAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute', 'value')
    list_filter = ('attribute',)


class AttributeOptionInline(admin.TabularInline):
    model = ProductAttributeOption


class ProductAttributeOptionGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'option_summary')
    inlines = [AttributeOptionInline]


class ProductAttributeOptionAdmin(admin.ModelAdmin):
    list_display = ('option','show_value', 'get_group_name',)
    list_filter = ('group',)

    def get_group_name(self, object):
        return object.group.name


admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductAttribute, ProductAttributeAdmin)
admin.site.register(ProductAttributeValue, ProductAttributeValueAdmin)
admin.site.register(ProductAttributeCategory, ProductAttributeCategoryAdmin)
admin.site.register(ProductAttributeOptionGroup, ProductAttributeOptionGroupAdmin)
admin.site.register(ProductAttributeOption, ProductAttributeOptionAdmin)

