from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("login/",sigin_user,name="login"),
    path("logout/",logout_user,name="logout"),
    path("register/",siginup_user,name="register"),
    path("profile/",profile,name="profile"),
 
]
