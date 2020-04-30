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


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key)) if isinstance(dictionary, dict) else None


@register.filter
def get_item_int(dictionary, key):
    return dictionary.get(int(key)) if isinstance(dictionary, dict) else None


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v

    return updated.urlencode()


@register.filter
def get_categories():
    return Category.objects.exclude(level=0)
