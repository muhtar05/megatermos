from django.shortcuts import render,Http404
from django.views import View
from core.models import Carousel,Page
from catalog.models import Product, ShockPriceProduct


def home(request):
    ctx = {}
    ctx['sales_leaders'] = Product.objects.all()[:4]
    ctx['carousel'] = Carousel.objects.all()
    ctx['sell_out'] = ShockPriceProduct.objects.all()[:4]
    return render(request,'index.html',ctx)


class PageView(View):

    def get(self, request, *args, **kwargs):
        ctx = {}
        try:
            ctx['page'] = Page.objects.get(url=kwargs.get('slug'))
        except Exception as e:
            raise Http404
        return render(request,'page.html',ctx)