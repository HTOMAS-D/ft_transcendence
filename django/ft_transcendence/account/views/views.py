from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

def loginView(request):
    return render(request, "account/login.html")


def logoutView(request):
    return render(request, "account/logout.html")


def registerView(request):
    return render(request, "account/register.html")