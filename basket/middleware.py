from django.core.signing import BadSignature, Signer
from django.utils.functional import SimpleLazyObject, empty
from basket.models import Basket


class BasketMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.cookies_to_delete = []
        request._basket_cache = None

        def load_full_basket():
            # print("load full basket")
            basket = self.get_basket(request)
            return basket

        def load_basket_hash():
            basket = self.get_basket(request)
            if basket.id:
                return self.get_basket_hash(basket.id)

        request.basket = SimpleLazyObject(load_full_basket)
        request.basket_hash = SimpleLazyObject(load_basket_hash)
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(self, request, response):
        cookies_to_delete = getattr(request, 'cookies_to_delete', [])
        for cookie_key in cookies_to_delete:
            response.delete_cookie(cookie_key)

        if not hasattr(request, 'basket'):
            return response

        # If the basket was never initialized we can safely return
        if (isinstance(request.basket, SimpleLazyObject)
                and request.basket._wrapped is empty):
            # print("return response")
            return response

        cookie_key = self.get_cookie_key(request)

        has_basket_cookie = (
            cookie_key in request.COOKIES
            and cookie_key not in cookies_to_delete)

        if (request.basket.id and not request.user.is_authenticated
                and not has_basket_cookie):
            cookie = self.get_basket_hash(request.basket.id)
            response.set_cookie(
                cookie_key, cookie,
                max_age=7 * 24 * 60 * 60,
                secure=False, httponly=True)
        return response

    def process_template_response(self, request, response):
        # print("process_template_response")
        if hasattr(response, 'context_data'):
            if response.context_data is None:
                response.context_data = {}
            if 'basket' not in response.context_data:
                response.context_data['basket'] = request.basket
            else:
                response.context_data['request_basket'] = request.basket
        return response

    def get_cookie_key(self, request):
        return 'open_basket'

    def get_cookie_basket(self, cookie_key, request, manager):
        basket = None
        if cookie_key in request.COOKIES:
            basket_hash = request.COOKIES[cookie_key]
            try:
                basket_id = Signer().unsign(basket_hash)
                basket = Basket.objects.get(pk=basket_id, owner=None,
                                            status=Basket.OPEN)
            except (BadSignature, Basket.DoesNotExist):
                request.cookies_to_delete.append(cookie_key)
        return basket

    def get_basket(self, request):
        if request._basket_cache is not None:
            return request._basket_cache

        num_baskets_merged = 0
        manager = Basket.open
        cookie_key = self.get_cookie_key(request)
        cookie_basket = self.get_cookie_basket(cookie_key, request, manager)

        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                basket, __ = manager.get_or_create(owner=request.user)
            except Basket.MultipleObjectsReturned:
                old_baskets = list(manager.filter(owner=request.user))
                basket = old_baskets[0]
                for other_basket in old_baskets[1:]:
                    self.merge_baskets(basket, other_basket)
                    num_baskets_merged += 1

            basket.owner = request.user

            if cookie_basket:
                self.merge_baskets(basket, cookie_basket)
                num_baskets_merged += 1
                request.cookies_to_delete.append(cookie_key)

        elif cookie_basket:
            # print("Anonymous user with a basket tied to the cookie")
            basket = cookie_basket
        else:
            # print("return basket empty")
            basket = Basket()

        request._basket_cache = basket

        if num_baskets_merged > 0:
            pass

        return basket

    def merge_baskets(self, master, slave):
        master.merge(slave, add_quantities=False)

    def get_basket_hash(self, basket_id):
        return Signer().sign(basket_id)


class StoreCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self,request, view_func, view_args, view_kwargs):
        print(view_kwargs)