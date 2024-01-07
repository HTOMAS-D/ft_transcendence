from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

# Create your views here.

def homepage(request):
    logger.info('!!! info test message !!!')
    return render(request, 'main/homepage.html')