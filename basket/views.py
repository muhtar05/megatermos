from django.shortcuts import render
from django.views.generic import View


class IndexView(View):
    template_name = 'basket.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request,self.template_name, ctx)
