from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name="website/welcome.html",authentication_form=UserLoginForm),name='welcome'),
]