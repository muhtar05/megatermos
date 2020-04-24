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

from catalog.models import Category, Product

class Command(BaseCommand):

    def add_image(self, img_url):
        print(img_url)
        curr_img_url = img_url.replace('/orig','')
        try:
            temp = ContentFile(urlopen(img_url,context=ssl.create_default_context(cafile=certifi.where())).read())
            ext_img = curr_img_url.split('.')
            ext_img = ext_img[-1]
            temp.name = '{}.{}'.format(uuid4().hex, ext_img)
            return temp
        except Exception as e:
            print(e)
            return None

    def handle(self, *args, **options):
        print("Add products")
        file_name = os.path.join(settings.BASE_DIR,'termos.xls')
        book = xlrd.open_workbook(file_name)
        sh = book.sheet_by_index(0)
        print("{0} {1} {2}".format(sh.name, sh.nrows, sh.ncols))
        print("Cell D30 is {0}".format(sh.cell_value(rowx=29, colx=5)))

        _root, _ = Category.objects.get_or_create(name='_root',slug='root', parent=None)

        categories = set()
        products = []
        artikuls = []
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

            products.append({
                'name': product_name,
                'artikul': product_artikul,
                'img_url': img_url,
                'price_opt': price_opt,
                'price': price,
                'old_price': old_price,
                'category_name': curr_cat,
                'category_slug': slugify(curr_cat),
            })


        for category in categories:
            sl_curr_cat = slugify(category)
            ext_cat = Category.objects.filter(slug=sl_curr_cat).first()
            if not ext_cat:
                new_cat = Category()
                new_cat.name = category
                new_cat.slug = sl_curr_cat
                new_cat.parent = _root
                new_cat.save()

        for prod in products:
            # print(prod.get('name'))
            artikul = prod.get('artikul')
            ext_prod = Product.objects.filter(artikul=artikul).first()
            if not ext_prod:
                need_category = Category.objects.filter(slug=prod.get('category_slug')).first()
                # print(need_category)
                new_prod = Product()
                new_prod.name = prod.get('name')
                new_prod.slug = slugify(prod.get('name'))
                new_prod.artikul = artikul
                new_prod.category = need_category
                new_prod.save()
                print(new_prod.pk)
            else:
                ext_prod.price_opt = prod.get('price_opt')
                ext_prod.price = prod.get('price')
                ext_prod.old_price = prod.get('old_price')
                if not ext_prod.img:
                    ext_prod.img = self.add_image(prod.get('img_url'))
                ext_prod.save()
                print('{} | {} | {}'.format(ext_prod.price_opt, ext_prod.price, ext_prod.old_price))
