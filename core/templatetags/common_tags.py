import datetime
from django import template
from django.contrib import messages
from catalog.models import Category
from core.models import Settings,Page
register = template.Library()


@register.inclusion_tag('footer.html', takes_context=True)
def footer_tag(context):
    return {
        'categories': Category.objects.exclude(level=0),
        'settings': Settings.objects.first(),
        'menu_footer_items': Page.objects.all(),
    }


@register.inclusion_tag('templatetags/menu_top.html', takes_context=True)
def menu_top(context):
    return {
        'menu_items': Page.objects.all()
    }
