from collections import OrderedDict
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse,Http404
from django.db.models import Q, F, Max, Min, Count
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from catalog.models import Product,Category, ProductAttribute, ProductAttributeValue, SeoModuleFilterUrl
from catalog.history import update


class IndexView(View):
    template_name = 'catalog/index.html'

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
    template_name = 'catalog/index.html'

    def get(self, request, *args, **kwargs):
        print("=====================GET========================")
        print(request.GET)
        slug = kwargs.get('slug')
        current_category = Category.objects.get(slug=slug)

        filter_options = ProductAttributeValue.objects.values_list('attribute_id', 'value_option_id'). \
            filter(Q(product__category_id=current_category.pk),
                   Q(value_option_id__isnull=False)).order_by('attribute__display_order')

        filter_result = OrderedDict()
        for f_opt in filter_options:
            current_ids = filter_result.get(f_opt[0], set())
            current_ids.add(f_opt[1])
            filter_result[f_opt[0]] = current_ids

        for key, val in filter_result.items():
            filter_result[key] = list(val)

        print(filter_result)

        all_products = Product.objects.filter(category=current_category).order_by('price')
        queries = []
        checked_options = {}
        for attr in ProductAttribute.objects.all():
            attr_param_new = request.GET.getlist(attr.code)
            if attr_param_new:
                checked_options[attr.code] = [int(ap) for ap in attr_param_new]
                queries.append(Q(attribute_values__attribute__code=attr.code,attribute_values__value_option__in=attr_param_new))

        q = Q()
        for query in queries:
            q = q | query

        all_products = all_products.filter(q)
        print(all_products.query)

        if request.GET.get('price-min'):
            all_products = all_products.filter(price__gte=request.GET.get('price-min'),
                                               price__lte=request.GET.get('price-max'))

        min_price = Product.objects.filter(category=current_category).aggregate(Min('price'))['price__min'] or 0
        max_price = Product.objects.filter(category=current_category).aggregate(Max('price'))['price__max'] or 0
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
        ctx['checked_options'] = checked_options
        ctx['filter_result'] = filter_result
        return render(request,self.template_name,ctx)


class ProductDetail(View):
    template_name = 'catalog/product.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        product = get_object_or_404(Product,pk=kwargs.get('pk'))
        ctx['product'] = product
        response = render(request, self.template_name,ctx)
        update(product, request, response)
        return response


class SearchPageView(View):
    template_name = 'catalog/search_page.html'

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('search_term')
        ctx = {}
        all_products = Product.objects.filter(Q(name__icontains='' + search_term + '')).order_by('price')
        ctx['search_term'] = search_term
        ctx['search_count'] = all_products.count()
        page = request.GET.get('page', 1)
        paginator = Paginator(all_products, 32)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(2)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        ctx['products'] = products

        return render(request,self.template_name,ctx)


class FilterAjaxView(View):

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        current_category = Category.objects.get(pk=category_id)

        filter_options = ProductAttributeValue.objects.values_list('attribute_id', 'value_option_id'). \
            filter(Q(product__category_id=current_category.pk),
                   Q(value_option_id__isnull=False)).order_by('attribute__display_order')

        filter_result = OrderedDict()
        for f_opt in filter_options:
            current_ids = filter_result.get(f_opt[0], set())
            current_ids.add(f_opt[1])
            filter_result[f_opt[0]] = current_ids

        for key, val in filter_result.items():
            filter_result[key] = list(val)

        print(filter_result)

        all_products = Product.objects.filter(category=current_category).order_by('price')
        queries = []
        checked_options = {}
        for attr in ProductAttribute.objects.all():
            attr_param_new = request.GET.getlist(attr.code)
            if attr_param_new:
                checked_options[attr.code] = [int(ap) for ap in attr_param_new]
                queries.append(Q(attribute_values__attribute__code=attr.code,attribute_values__value_option__in=attr_param_new))

        q = Q()
        for query in queries:
            q = q | query

        all_products = all_products.filter(q)
        from_price_min = int(request.GET.get('price-min'))
        from_price_max = int(request.GET.get('price-max'))
        all_products = all_products.filter(price__gte=from_price_min,price__lte=from_price_max)
        ctx = {}
        ctx['status'] = 'ok'
        ctx['num_count'] = all_products.count()
        return JsonResponse(ctx)


class FilterSeoUrlView(View):
    template_name = 'catalog/filter_seo_page.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        slug = kwargs.get('slug')
        current_category = Category.objects.get(slug=slug)
        filter_options = ProductAttributeValue.objects.values_list('attribute_id', 'value_option_id'). \
            filter(Q(product__category_id=current_category.pk)).order_by('attribute__display_order')
                   # Q(value_option_id__isnull=False)).order_by('attribute__display_order')

        filter_result = OrderedDict()
        for f_opt in filter_options:
            current_ids = filter_result.get(f_opt[0], set())
            current_ids.add(f_opt[1])
            filter_result[f_opt[0]] = current_ids

        for key, val in filter_result.items():
            filter_result[key] = list(val)
        need_url = "{0}/{1}".format(slug, kwargs.get('path'))
        print(need_url)

        seo_filter_url = SeoModuleFilterUrl.objects.filter(category=current_category,url=need_url).first()

        if not seo_filter_url:
            raise Http404

        brand_raw = seo_filter_url.parameters.split("_")


        all_products = Product.objects.filter(category=current_category).order_by('price')

        checked_options = {}
        queries = []
        checked_options[brand_raw[0]] = [int(opt) for opt in brand_raw[1:]]


        queries.append(
            Q(attribute_values__attribute__code=brand_raw[0], attribute_values__value_option__in=brand_raw[1:]))

        q = Q()
        for query in queries:
            q = q | query

        all_products = all_products.filter(q)

        min_price = Product.objects.filter(category=current_category).aggregate(Min('price'))['price__min'] or 0
        max_price = Product.objects.filter(category=current_category).aggregate(Max('price'))['price__max'] or 0
        page = request.GET.get('page', 1)
        paginator = Paginator(all_products, 32)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(2)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        ctx['products'] = products
        ctx['categories'] = Category.objects.exclude(level=0)
        ctx['current_category'] = current_category
        ctx['min_price_slider'] = min_price
        ctx['max_price_slider'] = max_price
        ctx['checked_options'] = checked_options
        ctx['filter_result'] = filter_result
        ctx['seo_filter_url'] = seo_filter_url
        return render(request, self.template_name, ctx)




