"""
URL configuration for authentication project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from oauth.views import oauth_test, oauth_callback
from login.views import login_test, authenticate_user
from totp.views import authenticate_totp

urlpatterns = [
    path('oauth/test', oauth_test),
    path('oauth/callback', oauth_callback),
    path('login/test', login_test),
    path('login/', authenticate_user),
    path('totp/', authenticate_totp)
]
