from datetime import datetime
from slugify import slugify
import time

from django.conf import settings
from django.db.models import Q, F, Max, Min, Count
from django.core.management.base import BaseCommand, CommandError

from catalog.models import (Category, Product, ProductAttributeValue,
                            ProductAttribute, ProductAttributeOption, SeoModuleFilterUrl,)


class Command(BaseCommand):

    def create_seo_filter_url(self, new_url, category, name, parameters):
        new_seo_url = SeoModuleFilterUrl()
        new_seo_url.url = new_url
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
                url = "{}/{}_{}"


                print(pr_attr.option_group.options.order_by('code').count())
                filter_options = ProductAttributeValue.objects.values_list('value_option_id'). \
                    filter(Q(product__category_id=cat.pk),
                           Q(attribute_id=pr_attr.pk),
                           Q(value_option_id__isnull=False))[:5]

                all_options = pr_attr.option_group.options.filter(id__in=filter_options).order_by('code')
                print(all_options)
                new_exclude = []
                for opt in all_options:
                    for option in all_options.exclude(code__in=new_exclude):
                        new_url = url.format(cat.slug,pr_attr.code,option.code)
                        ext_url = SeoModuleFilterUrl.objects.filter(url=new_url).first()
                        name = "{} | {}".format(cat.name, pr_attr.name)
                        parameters = "{}_{}".format(pr_attr.code, option.pk)
                        if not ext_url:
                            self.create_seo_filter_url(new_url,cat,name,parameters)

                        # new_exclude.append(option.code)

                        def generate_children(options_list, new_url,filter_options,new_parameters):
                            # print(options_list)
                            for other_option in options_list:
                                curr_url = new_url + "_" + other_option.code
                                parameters = new_parameters + "_" + str(other_option.pk)
                                generate_children(options_list.exclude(code=other_option.code), curr_url,
                                                  filter_options, parameters)
                                ext_url = SeoModuleFilterUrl.objects.filter(url=curr_url).first()

                                if not ext_url:
                                    # self.create_seo_filter_url(curr_url, cat, name, parameters)
                                    new_seo_url = SeoModuleFilterUrl()
                                    new_seo_url.url = curr_url
                                    new_seo_url.category = cat
                                    new_seo_url.name = name
                                    new_seo_url.parameters = parameters
                                    new_seo_url.save()

                                # print(curr_url)
                                # print('-----------------')




                        print(option)

                        new_exclude.append(option.code)
                        current_options = all_options.exclude(code__in=new_exclude)
                        generate_children(current_options, new_url, filter_options,parameters)
                        # break
                    # break
                    new_exclude.append(opt.code)

                break
            break

        for sm in SeoModuleFilterUrl.objects.all():
            sm.url = sm.url + "/"
            sm.save()
            # print(sm.url)
