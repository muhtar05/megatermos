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
        print("Attributes")
        file_name = os.path.join(settings.BASE_DIR,'termos.xls')
        book = xlrd.open_workbook(file_name)
        sh = book.sheet_by_index(0)
        print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
        print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=5)))

        _root, _ = Category.objects.get_or_create(name='_root',slug='root', parent=None)

        categories = set()
        products = []
        attributes = []
        for rx in range(sh.nrows):
            if rx == 0:
                continue
            curr_cat = sh.cell_value(rowx=rx, colx=5)
            categories.add(curr_cat)
            product_name = sh.cell_value(rowx=rx, colx=1)
            product_artikul = sh.cell_value(rowx=rx, colx=0)
            img_url = sh.cell_value(rowx=rx,colx=15)
            price_opt = sh.cell_value(rowx=rx, colx=16)
            price = sh.cell_value(rowx=rx, colx=17)
            old_price = sh.cell_value(rowx=rx, colx=18)
            material_case = sh.cell_value(rowx=rx, colx=10)
            material_flask = sh.cell_value(rowx=rx, colx=11)
            brand = sh.cell_value(rowx=rx, colx=2)
            volume = sh.cell_value(rowx=rx, colx=6)
            weight = sh.cell_value(rowx=rx, colx=7)
            height = sh.cell_value(rowx=rx, colx=12)
            diameter = sh.cell_value(rowx=rx, colx=13)
            keeps_warm = sh.cell_value(rowx=rx, colx=8)
            keeps_cold = sh.cell_value(rowx=rx, colx=9)

            attributes.append({
                # 'material_case':material_case,
                # 'material_flask':material_flask,
                # 'brand':brand,
                'volume':volume,
                'weight':weight,
                'height':height,
                'diameter':diameter,
                'keeps_warm':keeps_warm,
                'keeps_cold':keeps_cold,
            })

            products.append({
                'name': product_name,
                'artikul': product_artikul,
                'img_url': img_url,
                'price_opt': price_opt,
                'price': price,
                'old_price': old_price,
                'category_name': curr_cat,
                'category_slug': slugify(curr_cat),
                'material_case': material_case,
                'material_flask': material_flask,
                'brand': brand,
                'volume': volume,
                'weight': weight,
                'height': height,
                'diameter': diameter,
                'keeps_warm': keeps_warm,
                'keeps_cold': keeps_cold,
            })

        attributes_names = [
            # {'name':'Материал корпуса', 'code': 'material_case'},
            # {'name':'Материал колбы', 'code': 'material_flask'},
            # {'name':'Бренд', 'code': 'brand'},
            {'name':'Объем', 'code': 'volume'},
            {'name':'Вес', 'code': 'weight'},
            {'name':'Высота', 'code': 'height'},
            {'name':'Диаметр/ширина корпуса', 'code': 'diameter'},
            {'name':'Сохраняет тепло до, часов', 'code': 'keeps_warm'},
            {'name':'Сохраняет холод до, часов', 'code': 'keeps_cold'},
        ]

        codes_attributes = [attr_n.get('code') for attr_n in attributes_names]
        print(codes_attributes)

        for attr_n in attributes_names:
            prod_attr_option_group,_ = ProductAttributeOptionGroup.objects.get_or_create(name=attr_n.get('name'), code=attr_n.get('code'))
            ProductAttribute.objects.get_or_create(name=attr_n.get('name'),
                                                   code=attr_n.get('code'),
                                                   type='option',
                                                   option_group=prod_attr_option_group)

        print("===============Add ProductAttributeOption ============")
        for attr in attributes:
            print(attr)
            for c in codes_attributes:
                curr_val = attr.get(c)
                if curr_val:
                    attr_option_group = ProductAttributeOptionGroup.objects.get(code=c)
                    ProductAttributeOption.objects.get_or_create(group=attr_option_group,
                                                                 option=curr_val,
                                                                 show_value=curr_val.capitalize())


        print("===============Add ProductAttributeCategory for categories ============")
        for pr_attr in ProductAttribute.objects.all():
            for cat in Category.objects.exclude(level=0):
                ProductAttributeCategory.objects.get_or_create(attribute=pr_attr,
                                                               category=cat)

        print("===============Add ProductAttributeValue ============")
        for prod in products:
            artikul = prod.get('artikul')
            ext_prod = Product.objects.filter(artikul=artikul).first()
            for c in codes_attributes:
                print('{}={}'.format(c,prod.get(c)))
                pr_attr = ProductAttribute.objects.get(code=c)
                attr_option = ProductAttributeOption.objects.filter(group__code=c,option=prod.get(c)).first()
                if attr_option:
                    ProductAttributeValue.objects.get_or_create(attribute=pr_attr,
                                                            product=ext_prod,
                                                            value_option=attr_option)
