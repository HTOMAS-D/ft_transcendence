from .views import *
from django.http import HttpResponse

def homepage(request):
    return HttpResponse("You're at the homepage.")
