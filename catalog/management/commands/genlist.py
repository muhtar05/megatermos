from datetime import datetime
from slugify import slugify
import time
import itertools

from django.conf import settings
from django.db.models import Q, F, Max, Min, Count
from django.core.management.base import BaseCommand, CommandError

from catalog.models import (Category, Product, ProductAttributeValue,
                            ProductAttribute, ProductAttributeOption, SeoModuleFilterUrl,)


class Command(BaseCommand):

    def handle2(self, *args, **options):
        l1 = ['alfa','beta','gamma', 'delta', 'omega','p1','w2']
        l2 = ['alfa','beta','gamma', 'delta', 'omega','p1','w2']

        i = 0
        for elem in l1:
            current_urls = set()
            i +=1
            j = 0
            for other_elem in l2:
                j +=1
                if i != j:
                    print("{}_{}".format(elem,other_elem))
                    current_urls.add("{}_{}".format(elem,other_elem))
                print(elem + "_" + "_".join(l2[j:]))
                current_urls.add(elem + "_" + "_".join(l2[j:]))
            print(current_urls)
            break

    def handle(self, *args, **options):
        print("start")
        l1 = ['a','b','c','d']
        for i in itertools.product(l1, repeat=len(l1)):
            print(''.join(i))
