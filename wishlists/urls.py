from django.urls import path
from django.views.generic import TemplateView

from wishlists import views

app_name = 'wishlists'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('addproduct/', views.WishListCreateWithProductView.as_view(), name='add-product'),
    path('deleteproduct/', views.WishListDeleteWithProductView.as_view(), name='delete-product'),
]