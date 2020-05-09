from django.urls import path
from django.views.generic import TemplateView

from catalog import views

app_name = 'catalog'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('product/<int:pk>/reviews/create/', views.ReviewCreateView.as_view(), name='reviews-creater'),
    path('get_filter/', views.FilterAjaxView.as_view(), name='get-filter'),
    path('search/', views.SearchPageView.as_view(), name='search'),
    path('<slug:slug>_<int:pk>.html/', views.ProductDetail.as_view(), name='product-detail'),
    path('<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('<slug:slug>/<path:path>', views.FilterSeoUrlView.as_view(), name='filter-seo-url'),
]