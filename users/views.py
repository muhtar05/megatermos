from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View


class UserProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name)


class UserOrderHistoryView(View):
    template_name = 'users/orders_history.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request, self.template_name, ctx)


class UserRegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        ctx = {}
        return render(request,self.template_name,ctx)


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