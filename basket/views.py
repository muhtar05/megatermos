from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View

from catalog.models import Product


class IndexView(View):
    template_name = 'basket/index.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        print("===========Basket==============")
        print(request.basket)
        print(type(request.basket))
        ctx['basket'] = request.basket

        for line in request.basket.lines.all():
            print("==============Line=============")
            print(line)

        return render(request,self.template_name, ctx)


class BasketAddView(View):

    def post(self, request, *args, **kwargs):
        data = {}
        product_id = request.POST.get('product_id')
        print(product_id)
        product = Product.objects.get(pk=product_id)
        current_line,created  = self.request.basket.add_product(product, 1)
        data['status'] = 'ok'
        return JsonResponse(data)

