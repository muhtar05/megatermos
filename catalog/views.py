from django.shortcuts import render
from django.views.generic import View
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from catalog.models import Product,Category


class IndexView(View):
    template_name = 'catalog.html'

    def get(self, request, *args, **kwargs):
        all_products = Product.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(all_products, 32)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(2)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        ctx = {}
        ctx['products'] = products
        return render(request,self.template_name,ctx)


class CategoryDetailView(View):
    template_name = 'catalog.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        current_category = Category.objects.get(pk=pk)
        all_products = Product.objects.filter(category=pk)
        page = request.GET.get('page', 1)
        paginator = Paginator(all_products, 32)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(2)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        ctx = {}
        ctx['products'] = products
        ctx['categories'] = Category.objects.exclude(level=0)
        ctx['current_category'] = current_category
        return render(request,self.template_name,ctx)


class ProductDetail(View):
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

