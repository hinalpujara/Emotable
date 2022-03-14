from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name="website/welcome.html",authentication_form=UserLoginForm),name='welcome'),
    path('register/',views.register, name='register'),
    path('home/',views.home,name='home'),
    path('logout/',auth_views.LogoutView.as_view(template_name='website/logout.html'),name="logout") # temporary
]