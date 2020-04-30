from django.urls import path
from django.views.generic import TemplateView

from checkout import views

app_name = 'checkout'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('thank-you/', views.ThankYouView.as_view(), name='thank-you'),
]