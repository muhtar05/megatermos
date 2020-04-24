from django.urls import path
from django.views.generic import TemplateView

from catalog import views

app_name = 'catalog'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
]