from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils import timezone

from order.models import Order, Line


class IndexView(View):
    template_name = 'checkout/index.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request,self.template_name,ctx)

    def post(self, request, *args, **kwargs):
        ctx = {}
        basket = request.basket
        if basket.is_empty:
            raise ValueError("Корзина не должна быть пустой")

        order_number = 100000 + basket.id
        basket.freeze()
        total_price = 1000
        order_data = {'basket': basket,
                      'number': order_number,
                      'total_excl_tax': total_price,
                      'date_placed': timezone.now()
                      }

        # if request.user and request.user.is_authenticated():
        #     order_data['user_id'] = 1


        order = Order(**order_data)
        order.save()

        for line in basket.lines.all():
            product = line.product

            line_data = {
                'order': order,
                # Product details
                'product': product,
                'quantity': line.quantity,
                # Price details
                'line_price_excl_tax': line.price_excl_tax,
                'unit_retail_price': product.price,
            }
            current_line = Line.objects.filter(order=order, product=product)
            if current_line:
                current_line.update(**line_data)
                order_line = current_line
            else:
                order_line = Line._default_manager.create(**line_data)

        basket.submit()
        return redirect("checkout:thank-you")
        return render(request,self.template_name,ctx)


class ThankYouView(View):
    template_name = "checkout/thank_you.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
