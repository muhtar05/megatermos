import datetime
from django import template
from django.contrib import messages
from catalog.models import Category
register = template.Library()


@register.inclusion_tag('templatetags/catalog_menu.html', takes_context=True)
def catalog_menu(context):
    categories = Category.objects.exclude(level=0)
    return {
        'categories': categories,

    }