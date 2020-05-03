from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import View

from catalog.models import Product,ShockPriceProduct
from basket.models import Line


class IndexView(View):
    template_name = 'basket/index.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        print("===========Basket==============")
        print(request.basket)
        print(type(request.basket))
        ctx['basket'] = request.basket
        ctx['shock_price_products'] = ShockPriceProduct.objects.all()

        for line in request.basket.lines.all():
            print("==============Line=============")
            print(line)

        return render(request,self.template_name, ctx)


class BasketAddView(View):

    def post(self, request, *args, **kwargs):
        data = {}
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity',1))
        print(product_id)
        product = Product.objects.get(pk=product_id)
        current_line,created  = self.request.basket.add_product(product, quantity)
        data['status'] = 'ok'
        data['num_items'] = self.request.basket.num_items
        data['total_sum'] = self.request.basket.get_total_sum
        return JsonResponse(data)


class BasketDeleteView(View):

    def post(self, request, *args, **kwargs):
        data = {}
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        current_line = self.request.basket.lines.filter(product=product)
        current_line.delete()
        data['status'] = 'ok'
        data['num_items'] = self.request.basket.num_items
        data['total_sum'] = self.request.basket.get_total_sum
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
            product_id = request.POST.get('product_id')
            quantity = int(request.POST.get('value', 0))
            try:
                product = Product.objects.get(pk=product_id)
                current_line = self.request.basket.lines.get(product=product)
                if quantity > 0:
                    current_line.quantity= quantity
                    current_line.save()
                    from django.contrib.humanize.templatetags.humanize import intcomma
                    data = {
                        'num_items': self.request.basket.num_items,
                        'total_sum' : intcomma(int(self.request.basket.get_total_sum)),
                        'line_sum': intcomma(int(current_line.line_price_excl_tax)),
                        'val': quantity,
                        'status': 'ok',
                    }
                else:
                    data = {
                        'status': 'fail',
                    }
            except Exception as e:
                print(str(e))
                data = {
                    'status': 'fail',
                }
            return JsonResponse(data)
        else:
            data = {'status': 'This is not ajax'}
            return JsonResponse(data)


