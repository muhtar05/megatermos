import datetime
from django import template
from django.contrib import messages
from catalog.models import Category
from catalog import history
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


@register.inclusion_tag('templatetags/last_product_views.html',takes_context=True)
def recently_viewed_products(context, current_product=None):
    request = context['request']
    products = history.get(request)[:10]
    if current_product:
        products = [p for p in products if p != current_product]
    return {'products': products}
