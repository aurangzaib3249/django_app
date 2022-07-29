from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("login/",sigin_user,name="login"),
    path("logout/",logout_user,name="logout"),
    path("register/",siginup_user,name="register"),
    path("profile/",profile,name="profile"),
    path("queries/",create_query,name="create_query"),
    path("create_query",create_query,name="queries"),
    path("get_or_create_query",get_or_create_query,name="get_or_create_query"),
    path("update_or_create_query",update_or_create_query,name="update_or_create_query"),
    path("bulk_create_query",bulk_create_query,name="bulk_create_query"),
    path("bulk_update_query",bulk_update_query,name="bulk_update_query"),
    path("select_related_query",select_related_query,name="select_related_query"),
    path("prefetch_related_query",prefetch_related_query,name="prefetch_related_query"),
 
]
