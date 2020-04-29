from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View

from catalog.models import Product
from basket.models import Line


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


class RemoveBasketLine(View):

    def get(self, request, *args, **kwargs):
        line_pk = kwargs.get('pk')
        print(request.basket.lines.filter(pk=line_pk).delete())
        return redirect('basket:index')


class ChangeQuantity(View):
    """
     Изменение количество заказываемых товаров в корзине
    """

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            print("=====POST=====")
            print(request.POST)
            pk = request.POST.get('line_pk')
            quantity = request.POST.get('value', 0)

            Line.objects.filter(pk=pk, basket=request.basket).update(quantity=int(quantity))
            data = {
                'num_items': self.request.basket.num_items,
                'val': quantity,
                'status': 'ok',
            }
            return JsonResponse(data)
        else:
            data = {'status': 'This is not ajax'}
            return JsonResponse(data)


