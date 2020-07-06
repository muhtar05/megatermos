from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from users.forms import UserForm, RegisterForm
from order.models import Order


class UserProfileView(LoginRequiredMixin,View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class UserOrderHistoryView(LoginRequiredMixin,View):
    template_name = 'users/orders_history.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        if request.user.is_admin:
            orders = Order.objects.all()
        else:
            orders = request.user.orders.all()
        ctx['orders'] = orders
        return render(request, self.template_name, ctx)


class UserRegisterView(View):
    template_name = 'users/register.html'
    user_form =RegisterForm

    def get(self, request, *args, **kwargs):
        ctx = {}
        ctx['user_form'] = self.user_form()
        return render(request,self.template_name,ctx)

    def post(self, request, *args, **kwargs):
        ctx = {}
        user_form = self.user_form(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            return redirect('/')
        else:
            ctx['user_form'] = user_form

        return render(request, self.template_name, ctx)


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request,self.template_name,ctx)

    def post(self, request, *args, **kwargs):
        ctx = {}
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:profile')
        else:
            ctx['errors'] = []
        return render(request,self.template_name,ctx)


def logout_view(request):
    logout(request)
    return redirect('/')