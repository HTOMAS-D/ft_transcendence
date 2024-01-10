from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from ..forms import CreateUserForm

def loginView(request):
    if request.user.is_authenticated:
        return redirect('main:homepage')
    registerForm = CreateUserForm()
        
    context = {
        'registerForm': registerForm,
        }
    return render(request, "account/login.html", context)


def doLoginView(request):
    if request.user.is_authenticated:
        return redirect('main:homepage')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': 'Invalid credentials'})
        
    return render(request, "account/login.html")



def doLogoutView(request):
    if request.method == 'GET':
        logout(request)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'errors': 'No user to logout'})
    


def registerView(request):
    if request.user.is_authenticated:
        return redirect('main:homepage')
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
