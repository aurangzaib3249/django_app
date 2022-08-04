from cgitb import handler
from datetime import datetime
from django.forms import PasswordInput
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.messages import constants 
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView,DeleteView
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
MESSAGE_TAGS = {
    constants.DEBUG: 'info',
    constants.INFO: 'info',
    constants.SUCCESS: 'success',
    constants.WARNING: 'warning',
    constants.ERROR: 'danger',
}
@login_required(login_url='login')
def home(request):
    return render(request,"home.html")
@require_http_methods(["POST","GET"])
def sigin_user(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        if email and password:
            print(email,password)
            user=authenticate(username=email,password=password)
            if user:
                if user.last_login:
                    messages.success(request,"Welcome to django app")
                else:
                    messages.success(request,"Welcome back to django app")
                login(request,user)
                return redirect("home")
                
            else:
                messages.error(request,"Username or password is invalid!")
        else:
            messages.error(request,"Both fields are required!")
    return render(request,"login.html")

def siginup_user(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form=UserForm()
    return render(request,"register.html",{"form":form})
   
@login_required(login_url='login')

def profile(request):
    user=request.user
    if request.method=="POST":
        form=UserUpdateForm(request.POST or None,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request,"info updated")
            return redirect("profile")
    else:
        form=UserUpdateForm(instance=user)
   
    return render(request,"profile.html",{"form":form})
def logout_user(request):
    logout(request)
    messages.success(request,"user logout!")
    return redirect ("login")

class list_view(LoginRequiredMixin,ListView):
    model=User
    paginate_by=1
    
    #context_object_name="users"
    
    #override all functions
    def get_login_url(self) -> str:
        return "login"
    def get_queryset(self):
        obj=User.objects.filter(is_active=True)
        return obj
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["total_users"]=self.get_queryset().all().count()
        return context
    def get_template_names(self):
        return "list_view.html"
    def get_context_object_name(self, object_list):
        return "users"
    def dispatch(self, request, *args, **kwargs):
        #Use dispatch function for auth and request method handle, now I comment because i am using  LoginRequiredMixin
        """if not request.user.is_authenticated:
            if request.method.lower() not in ["get"]:
                return HttpResponse("{} is not allowed".format(request.method.lower()) )
            return HttpResponseRedirect('login')"""
        return super().dispatch(request, *args, **kwargs)
    

class detail_view(DetailView):
    model=User
    template_name="user_detail.html"
    context_object_name="user"
    
    def get_context_data(self ,**kwargs):
        context=super().get_context_data()
        context["time"]=datetime.now()
        return context