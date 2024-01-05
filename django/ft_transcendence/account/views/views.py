from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from ..forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def loginView(request):
    registerForm = CreateUserForm()
        
    context = {
        'registerForm': registerForm,
        }
    return render(request, "account/login.html", context)


def logoutView(request):
    return render(request, "account/logout.html")



def registerView(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'{user} created with success!')
            return JsonResponse({'status': 'success'})
        else:
            print('Not valid form')
            errors = [str(error) for error in form.errors.values()]
            return JsonResponse({'status': 'error', 'errors': errors})
    else:
        registerForm = CreateUserForm()
        context = {'registerForm': registerForm}
        return render(request, "account/login.html", context)
