from django.urls import path
from django.views.generic import TemplateView

from basket import views

app_name = 'basket'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/<int:pk>/', views.BasketAddView.as_view(), name='add-product'),
    path('delete/<int:pk>/', views.BasketDeleteView.as_view(), name='delete-product'),
    path('remove/<int:pk>/', views.RemoveBasketLine.as_view(), name='remove-line'),
    path('changequantity/', views.ChangeQuantity.as_view(), name='changequantity'),
]