from django.urls import path
from django.views.generic import TemplateView

from users import views

app_name = 'users'


urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    path('profile/orders/', views.UserOrderHistoryView.as_view(), name='orders-history'),
]