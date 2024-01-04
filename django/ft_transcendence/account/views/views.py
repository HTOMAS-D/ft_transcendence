from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..forms import CreateUserForm

def loginView(request):
    registerForm = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            
        
    context = {
        'registerForm': registerForm,
        }
    return render(request, "account/login.html", context)


def logoutView(request):
    return render(request, "account/logout.html")


def registerView(request):
    return render(request, "account/register.html")