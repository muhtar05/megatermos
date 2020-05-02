from datetime import datetime
from slugify import slugify

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from catalog.models import (Category, Product, ProductAttributeValue,
                            ProductAttribute, ProductAttributeOption, SeoModuleFilterUrl,)


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("Generate filter urls")

        SeoModuleFilterUrl.objects.all().delete()

        for pr_attr in ProductAttribute.objects.all():
            print(pr_attr.code)
            print(pr_attr.option_group)
            for cat in Category.objects.exclude(level=0):
                print(cat.slug)
                url = "{}/{}_{}"
                exclude_list = []
                for option in pr_attr.option_group.options.order_by('code'):
                    print(option.code)
                    new_url = url.format(cat.slug,pr_attr.code,option.code)
                    print('-----------------')
                    print(new_url)
                    ext_url = SeoModuleFilterUrl.objects.filter(url=new_url).first()
                    if not ext_url:
                        new_seo_url = SeoModuleFilterUrl()
                        new_seo_url.url = new_url
                        new_seo_url.category = cat
                        new_seo_url.name = "{} | {}".format(cat.name, pr_attr.name)
                        new_seo_url.parameters = "{}_{}".format(pr_attr.code,option.pk)
                        new_seo_url.save()
                    print('-----------------')
                    exclude_list.append(option.code)
                    for other_option in pr_attr.option_group.options.exclude(code__in=exclude_list).order_by('code'):
                        curr_url = "{}_{}".format(new_url,other_option.code)
                        print('-----------------')
                        print(new_url)
                        ext_url = SeoModuleFilterUrl.objects.filter(url=curr_url).first()
                        if not ext_url:
                            new_seo_url = SeoModuleFilterUrl()
                            new_seo_url.url = curr_url
                            new_seo_url.category = cat
                            new_seo_url.name = "{} | {}".format(cat.name, pr_attr.name)
                            new_seo_url.parameters = "{}_{}_{}".format(pr_attr.code,option.pk,other_option.pk)
                            new_seo_url.save()
                        print('-----------------')
                break
            break