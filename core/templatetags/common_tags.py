import datetime
import re
from django import template
from django.contrib import messages
from catalog.models import Category
from wishlists.models import WishList
from core.models import Settings,Page, City
register = template.Library()


@register.inclusion_tag('footer.html', takes_context=True)
def footer_tag(context):
    settings = Settings.objects.first()
    return {
        'categories': Category.objects.exclude(level=0),
        "settings": settings,
        "settings_phone_digits": re.sub('\D', '', settings.phone),
        'menu_footer_items': Page.objects.all(),
    }


@register.inclusion_tag('all_modals.html', takes_context=True)
def all_modals_tag(context):
    settings = Settings.objects.first()
    return {
        "settings": settings,
        'cities': City.objects.all(),
    }


@register.inclusion_tag('header.html', takes_context=True)
def header_tag(context):
    COOKIE_NAME = 'wishlist_product'
    request = context.get('request')
    settings = Settings.objects.first()
    try:
        current_city = City.objects.get(pk=request.COOKIES['city_pk'])
    except Exception as e:
        current_city = City.objects.first()
    try:
        wish_list = WishList.objects.get(hash_id=request.COOKIES[COOKIE_NAME])
        wish_list_items = wish_list.lines.count()
    except Exception as e:
        wish_list_items = 0
    return {
        "request": context.get('request'),
        "wish_list_items": wish_list_items,
        "settings": settings,
        "current_city": current_city,
        "settings_phone_digits": re.sub('\D', '', settings.phone)
    }


@register.inclusion_tag('templatetags/menu_top.html', takes_context=True)
def menu_top(context):
    return {
        'menu_items': Page.objects.all()
    }


@register.filter
def only_digits(value):
    return re.sub('\D', '', value)