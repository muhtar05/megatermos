from datetime import datetime
from slugify import slugify
import time

from itertools import product,combinations

from django.conf import settings
from django.db.models import Q, F, Max, Min, Count
from django.core.management.base import BaseCommand, CommandError

from catalog.models import (Category, Product, ProductAttributeValue,
                            ProductAttribute, ProductAttributeOption,
                            SeoModuleFilterUrl, QuickLink, SitemapFilter,)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Create quick links")
        sitemap_filter_items = SitemapFilter.objects.all()
        for s_item in sitemap_filter_items:
            print(s_item)
            product_attr = s_item.attribute
            for opt_val in product_attr.option_group.options.all():
                all_products = Product.objects.filter(category=s_item.category)
                all_products = all_products.filter(
                        Q(attribute_values__attribute__code=product_attr.code,
                          attribute_values__value_option__in=[opt_val.pk]))

                if all_products.count() > 0:
                    need_url = "/catalog/{0}/{1}_{2}/".format(s_item.category.slug, product_attr.code, opt_val.code)
                    quick_link = QuickLink.objects.filter(url=need_url).first()
                    if not quick_link:
                        new_quick_link = QuickLink()
                        new_quick_link.category = s_item.category
                        new_quick_link.name = "{} {}".format(s_item.category.name, opt_val.option)
                        new_quick_link.url = need_url
                        new_quick_link.save()
                        print(new_quick_link.url)
