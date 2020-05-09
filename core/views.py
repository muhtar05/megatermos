from django.shortcuts import render, redirect
from django.views import View
from core.models import City


class SetCityView(View):

    def post(self, request, *args, **kwargs):
        city_id = request.POST.get('city')
        city_code = City.objects.get(pk=city_id)
        response = redirect('/')
        response.set_cookie(
            'city_pk', city_code.pk
        )
        return response

