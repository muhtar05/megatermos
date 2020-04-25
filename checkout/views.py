from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = 'checkout/index.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request,self.template_name,ctx)


class PaymentCreateView(View):
    def get(self, request, *args, **kwargs):
        pass
