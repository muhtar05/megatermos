from datetime import datetime
import csv
import json
import certifi
import ssl
from uuid import uuid4
from urllib.request import urlopen
from slugify import slugify
import os
import xlrd

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile

from catalog.models import (Category, Product, ProductAttributeOptionGroup,
                            ProductAttributeOption, ProductAttribute,ProductAttributeValue,ProductAttributeCategory,)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for opt in ProductAttributeOption.objects.filter(group__code='volume'):
            opt_value = opt.option.replace('л','').replace(' ','')
            opt.code = opt_value
            opt.save()
            print(opt_value)


        for opt in ProductAttributeOption.objects.filter(group__code='weight'):
            opt_value = opt.option.replace('г','').replace(' ','')
            opt.code = opt_value
            opt.save()
            print(opt_value)

        for opt in ProductAttributeOption.objects.filter(group__code='height'):
            opt_value = opt.option.replace('см','').replace(' ','')
            opt.code = opt_value
            opt.save()
            print(opt_value)

        for opt in ProductAttributeOption.objects.filter(group__code='diameter'):
            opt_value = opt.option.replace('см','').replace(' ','')
            opt.code = opt_value
            opt.save()
            print(opt_value)

        for opt in ProductAttributeOption.objects.filter(group__code='keeps_warm'):
            opt_value = opt.option.replace('ч','').replace(' ','')
            opt.code = opt_value
            opt.save()
            print(opt_value)

        for opt in ProductAttributeOption.objects.filter(group__code='keeps_cold'):
            opt_value = opt.option.replace('ч','').replace(' ','')
            opt.code = opt_value
            opt.save()
            print(opt_value)


