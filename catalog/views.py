from collections import OrderedDict
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse,Http404
from django.db.models import Q, F, Max, Min, Count
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from catalog.models import (Product,Category, ProductAttribute, ProductAttributeValue,
                            SeoModuleFilterUrl,ProductAttributeOption, ProductAttributeOptionGroup,)
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

        all_products = Product.objects.filter(category=current_category)
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

        order_val = request.GET.get('order')

        if order_val:
            if order_val == 'price_asc':
                all_products = all_products.order_by('price')
                current_order = 'price_asc'
            elif order_val == 'price_desc':
                all_products = all_products.order_by('-price')
                current_order = 'price_desc'
            else:
                all_products = all_products.order_by('date_created')
                current_order = 'new'
        else:
            all_products = all_products.order_by('date_created')
            current_order = 'new'

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
        ctx['current_order'] = current_order
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


def get_filter_result(category_id):
    filter_options = ProductAttributeValue.objects.values_list('attribute_id', 'value_option_id'). \
        filter(Q(product__category_id=category_id)).order_by('attribute__display_order')

    filter_result = OrderedDict()
    for f_opt in filter_options:
        current_ids = filter_result.get(f_opt[0], set())
        current_ids.add(f_opt[1])
        filter_result[f_opt[0]] = current_ids

    for key, val in filter_result.items():
        filter_result[key] = list(val)
    return filter_result


class FilterAjaxView(View):

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        current_category = Category.objects.get(pk=category_id)
        all_products = Product.objects.filter(category=current_category).order_by('price')
        for attr in ProductAttribute.objects.all():
            attr_param_new = request.GET.getlist(attr.code)
            if attr_param_new:
                all_products = all_products.filter(Q(attribute_values__attribute__code=attr.code,
                                      attribute_values__value_option__in=attr_param_new))

        all_products = all_products.filter(price__gte=int(request.GET.get('price-min')),
                                           price__lte=int(request.GET.get('price-max')))
        ctx = {}
        ctx['status'] = 'ok'
        ctx['num_count'] = all_products.count()
        return JsonResponse(ctx)


class FilterSeoUrlView(View):
    template_name = 'catalog/filter_seo_page.html'

    def get_filter_result(self, current_category):
        filter_options = ProductAttributeValue.objects.values_list('attribute_id', 'value_option_id'). \
            filter(Q(product__category_id=current_category.pk)).order_by('attribute__display_order')

        filter_result = OrderedDict()
        for f_opt in filter_options:
            current_ids = filter_result.get(f_opt[0], set())
            current_ids.add(f_opt[1])
            filter_result[f_opt[0]] = current_ids

        for key, val in filter_result.items():
            filter_result[key] = list(val)
        return filter_result

    def get(self, request, *args, **kwargs):
        ctx = {}
        slug = kwargs.get('slug')
        current_category = Category.objects.get(slug=slug)
        filter_result = self.get_filter_result(current_category)
        parse_url = ""
        parse_url_list = [part for part in kwargs.get('path').split('/') if part]

        price_to, price_from = None, None

        h1_title = "{} ".format(current_category.name)

        for part in parse_url_list:
            if "price_to"in part:
                price_to_raw = part.replace("price_to_","")
                if price_to_raw:
                    price_to = int(price_to_raw)
            elif "price_from"  in part:
                price_from_raw = part.replace("price_from_","")
                if price_from_raw:
                    price_from = int(price_from_raw)
            else:
                part_list = part.split('_')
                product_attr = ProductAttribute.objects.get(code=part_list[0])
                options_names = list(product_attr.option_group.options.values_list('option',flat=True).filter(code__in=part_list[1:]))
                h1_title += " для {} {}".format(product_attr.name.lower(), ','.join(options_names))
                parse_url += part + "/"

        need_url = "{0}/{1}".format(slug, parse_url)
        seo_filter_url = SeoModuleFilterUrl.objects.filter(category=current_category,url=need_url).first()

        if not seo_filter_url:
            seo_text = "{}".format(current_category.name)
            seo_filter_url = SeoModuleFilterUrl.objects.create(
                name="New url",
                url=need_url,
                h1=h1_title,
                seo_text=seo_text,
                category=current_category,
                parameters=parse_url.strip("/")
            )

        all_products = Product.objects.filter(category=current_category)
        checked_options = {}
        queries = []
        all_arrtibutes = seo_filter_url.parameters.split("/")
        for attr in all_arrtibutes:
            parameters_raw = attr.split("_")
            current_prod_attr = ProductAttribute.objects.get(code=parameters_raw[0])
            parameters_ids = [current_prod_attr.option_group.options.get(code=opt).pk for opt in parameters_raw[1:]]
            checked_options[parameters_raw[0]] = parameters_ids
            queries.append(
                Q(attribute_values__attribute__code=parameters_raw[0], attribute_values__value_option__in=parameters_ids))

        for query in queries:
            all_products = all_products.filter(query)

        print(all_products.query)

        min_price = Product.objects.filter(category=current_category).aggregate(Min('price'))['price__min'] or 0
        max_price = Product.objects.filter(category=current_category).aggregate(Max('price'))['price__max'] or 0

        price_min = price_from if price_from else min_price
        price_max = price_to if price_to else max_price

        all_products = all_products.filter(price__gte=price_min,price__lte=price_max)

        order_val = request.GET.get('order')
        if order_val:
            if order_val == 'price_asc':
                all_products = all_products.order_by('price')
                current_order = 'price_asc'
            elif order_val == 'price_desc':
                all_products = all_products.order_by('-price')
                current_order = 'price_desc'
            else:
                all_products = all_products.order_by('date_created')
                current_order = 'new'
        else:
            all_products = all_products.order_by('date_created')
            current_order = 'new'

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
        ctx['current_order'] = current_order
        return render(request, self.template_name, ctx)




