from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.db.models import Q, F, Max, Min, Count
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
        slug = kwargs.get('slug')
        current_category = Category.objects.get(slug=slug)
        all_products = Product.objects.filter(category=current_category).order_by('price')
        min_price = all_products.aggregate(Min('price'))['price__min'] or 0
        max_price = all_products.aggregate(Max('price'))['price__max'] or 0
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
        ctx['min_price_slider'] = min_price
        ctx['max_price_slider'] = max_price
        return render(request,self.template_name,ctx)


class ProductDetail(View):
    template_name = 'product.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        ctx['product'] = get_object_or_404(Product,pk=kwargs.get('pk'))
        return render(request, self.template_name,ctx)

