import pymorphy2
from django.db.models import F
from django.core.management.base import BaseCommand
from catalog.models import ProductAttributeOption, ProductAttribute


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("set genitive names")
        ProductAttribute.objects.filter(prefix_name__isnull=True).update(prefix_name=' ')
        options = ProductAttributeOption.objects.exclude(group__code__in=['material_flask', 'material_case'])

        options.update(genitive_name=F('option'))
        morph = pymorphy2.MorphAnalyzer()
        for opt in ProductAttributeOption.objects.filter(group__code__in=['material_flask', 'material_case']):
            curr_option = morph.parse(opt.option)[0]
            opt.genitive_name = curr_option.inflect({'gent'})[0]
            opt.save()
            print(opt.genitive_name)
