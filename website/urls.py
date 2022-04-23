from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
from .views import activate

urlpatterns = [
    path('',auth_views.LoginView.as_view(template_name="website/welcome.html",authentication_form=UserLoginForm,redirect_authenticated_user=True),name='welcome'),
    path('register/',views.register, name='register'),
    path('home/',views.home,name='home'),
    path('logout/',auth_views.LogoutView.as_view(template_name='website/logout.html'),name="logout"), # temporary
    path('googleRegister/',views.googleRegister,name='googleRegister'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activate, name='activate'),
    path('edit/', views.edit_prof, name='edit-profile'),
    path('unlikePost/<int:pk>',views.unlikePost,name='unlikePost'),
    path('likePost/<int:pk>',views.likePost,name='likePost'),
    path('postComment/',views.postComment,name='postComment'),
    path('profile/<str:username>',views.userProfile,name='userProfile'),
    # path('', views.index, name='index'),
    # path('<str:post_id>/', views.room, name='room'),
]