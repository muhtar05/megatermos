from django.urls import path
from django.views.generic import TemplateView

from core import views

app_name = 'core'


urlpatterns = [
    path('setcity', views.SetCityView.as_view(), name='set-city'),
]