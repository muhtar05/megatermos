from django.urls import path
from django.views.generic import TemplateView

from basket import views

app_name = 'basket'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/<int:pk>/', views.BasketAddView.as_view(), name='add-product'),
]