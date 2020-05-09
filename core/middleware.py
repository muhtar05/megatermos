from core.models import City


class CityChoiceMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if 'city_pk' not in request.COOKIES:
            try:
                city_code = City.objects.first()
                if city_code:
                    response.set_cookie('city_pk', city_code.pk)
            except Exception as e:
                print(e)
        return response