from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

# Create your views here.

# @login_required(login_url='account:login')
# def homepage(request):
#     logger.info('!!! info test message !!!')
#     return render(request, 'main/homepage.html')