import uuid
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from catalog.models import Product, Category
from wishlists.models import WishList
COOKIE_NAME = 'wishlist_product'


class IndexView(View):
    template_name = 'wishlists/index.html'

    def get(self, request,*args, **kwargs):
        ctx = {}
        wish_list = WishList.objects.get(hash_id=request.COOKIES[COOKIE_NAME])
        ctx['wish_list'] = wish_list
        ctx['categories'] = Category.objects.exclude(level=0)
        return render(request, self.template_name, ctx)


class WishListCreateWithProductView(View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        data = {}
        if not request.COOKIES.get(COOKIE_NAME):
            hash_id = uuid.uuid4().hex
            wish_list, created = WishList.objects.get_or_create(hash_id=hash_id)
            wish_list.add(product)
            data['num_items'] = wish_list.lines.count()
            response = JsonResponse(data)
            response.set_cookie('wishlist_product',
                                hash_id,
                                max_age=7 * 24 * 60 * 60,
                                secure=False,
                                httponly=True)
        else:
            hash_id = request.COOKIES[COOKIE_NAME]
            wish_list, created = WishList.objects.get_or_create(hash_id=hash_id)
            wish_list.add(product)
            data['num_items'] = wish_list.lines.count()
            response = JsonResponse(data)

        return response


class WishListDeleteWithProductView(View):

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        data = {}
        hash_id = request.COOKIES[COOKIE_NAME]
        wish_list, created = WishList.objects.get_or_create(hash_id=hash_id)
        lines = wish_list.lines.filter(product=product)
        if len(lines) > 0:
            lines.delete()
        data['num_items'] = wish_list.lines.count()
        return JsonResponse(data)
