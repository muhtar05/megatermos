from django.urls import path
from django.views.generic import TemplateView

from catalog import views

app_name = 'catalog'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    # path('demo/<int:pk>/', views.ConsultationDemoView.as_view(), name='demo'),
]