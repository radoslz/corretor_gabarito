from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("exams:dashboard")


def login_view(request):
    view = UserLoginView.as_view()
    return view(request)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")