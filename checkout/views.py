from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils import timezone

from order.models import Order, Line
from users.forms import UserForm
from order.forms import ShippingAddressForm


class IndexView(View):
    template_name = 'checkout/index.html'
    user_form = UserForm
    shipping_address_form = ShippingAddressForm

    def get(self, request, *args, **kwargs):
        ctx = {}
        basket = request.basket
        # if basket.is_empty:
        #     raise ValueError("Корзина не должна быть пустой")
        ctx['user_form'] = self.user_form()
        ctx['shipping_address_form'] = self.shipping_address_form()
        return render(request,self.template_name,ctx)

    def post(self, request, *args, **kwargs):
        ctx = {}
        basket = request.basket
        if basket.is_empty:
            raise ValueError("Корзина не должна быть пустой")

        shipping_address_form = self.shipping_address_form(request.POST)
        user_form = self.user_form(request.POST)

        if shipping_address_form.is_valid() and user_form.is_valid():
            order_number = 100000 + basket.id
            basket.freeze()
            total_price = 1000
            shipping_address = shipping_address_form.save()
            new_user = user_form.save(commit=False)
            new_user.set_password("123456m")
            new_user.save()
            order_data = {'basket': basket,
                          'number': order_number,
                          'total_excl_tax': total_price,
                          'shipping_address': shipping_address,
                          'user': new_user,
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
        else:
            ctx['user_form'] = user_form
            ctx['shipping_address_form'] = shipping_address_form

        return render(request,self.template_name,ctx)


class ThankYouView(View):
    template_name = "checkout/thank_you.html"

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)
