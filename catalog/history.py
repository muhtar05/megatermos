import json
from catalog.models import Product
RECENTLY_VIEWED_COOKIE_NAME = 'recently_history'

def get(request):
    """
    Return a list of recently viewed products
    """
    ids = extract(request)

    # Reordering as the ID order gets messed up in the query
    product_dict = Product.browsable.in_bulk(ids)
    ids.reverse()
    return [product_dict[id] for id in ids if id in product_dict]


def extract(request, response=None):
    ids = []
    cookie_name = RECENTLY_VIEWED_COOKIE_NAME
    if cookie_name in request.COOKIES:
        try:
            ids = json.loads(request.COOKIES[cookie_name])
        except ValueError:
            # This can occur if something messes up the cookie
            if response:
                response.delete_cookie(cookie_name)
        else:
            # Badly written web crawlers send garbage in double quotes
            if not isinstance(ids, list):
                ids = []
    return ids


def add(ids, new_id):
    max_products = 20
    if new_id in ids:
        ids.remove(new_id)
    ids.append(new_id)
    if (len(ids) > max_products):
        ids = ids[len(ids) - max_products:]
    return ids


def update(product, request, response):
    ids = extract(request, response)
    updated_ids = add(ids, product.id)
    response.set_cookie(
        RECENTLY_VIEWED_COOKIE_NAME,
        json.dumps(updated_ids),
        max_age=7 * 24 * 60 * 60,
        secure=False,
        httponly=True
    )