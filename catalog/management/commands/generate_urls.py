from datetime import datetime
from slugify import slugify
import time

from itertools import product,combinations

from django.conf import settings
from django.db.models import Q, F, Max, Min, Count
from django.core.management.base import BaseCommand, CommandError

from catalog.models import (Category, Product, ProductAttributeValue,
                            ProductAttribute, ProductAttributeOption, SeoModuleFilterUrl,)


class Command(BaseCommand):

    def create_seo_filter_url(self, new_url, category, name, parameters):
        new_seo_url = SeoModuleFilterUrl()
        new_seo_url.url = new_url + "/"
        new_seo_url.category = category
        new_seo_url.name = name
        new_seo_url.parameters = parameters
        new_seo_url.save()

    def handle(self, *args, **options):
        print("Generate filter urls")

        SeoModuleFilterUrl.objects.all().delete()

        for pr_attr in ProductAttribute.objects.all():
            print(pr_attr.code)
            print(pr_attr.option_group)

            for cat in Category.objects.exclude(level=0):
                print(cat.slug)
                url = "{}/{}_".format(cat.slug,pr_attr.code)
                filter_options = ProductAttributeValue.objects.values_list('value_option_id'). \
                    filter(Q(product__category_id=cat.pk),
                           Q(attribute_id=pr_attr.pk),
                           Q(value_option_id__isnull=False))

                all_options = pr_attr.option_group.options.filter(id__in=filter_options).order_by('code')
                all_codes = [opt.code for opt in all_options]

                i = len(all_codes) if len(all_codes) < 5 else 4
                name = "{} | {}".format(cat.name, pr_attr.name)
                parameters = ""
                while i > 0:
                    print(i)
                    j = 0
                    for el in combinations(all_codes, i):
                        curr_codes = '_'.join(el)
                        parameters = pr_attr.code + "_" +  curr_codes
                        self.create_seo_filter_url(url + curr_codes, cat, name, parameters)
                        j +=1
                    print("j=={}".format(j))

                    i -= 1