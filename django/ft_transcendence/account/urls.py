from django.urls import path
from .views import views

app_name="account"
urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('do-login/', views.doLoginView, name='doLogin'),
    path('do-logout/', views.doLogoutView, name='doLogout'),
    path('register/', views.registerView, name='register'),
]
