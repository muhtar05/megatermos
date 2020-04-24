from django.shortcuts import render
from catalog.models import Product


def home(request):
    ctx = {}
    ctx['sales_leaders'] = Product.objects.all()[:4]
    ctx['sell_out'] = Product.objects.all()[:4]
    return render(request,'index.html',ctx)