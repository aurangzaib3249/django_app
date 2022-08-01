from unicodedata import name
from xml.etree.ElementInclude import include
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.messages import constants 
from django.contrib import messages
from django.conf import settings
from django.core import management
from django.core.management.commands import makemigrations,migrate
from django_app.settings import *
db_dict={}
#settings.DATABASES['default']['NAME'] = "admin1"
MESSAGE_TAGS = {
    constants.DEBUG: 'info',
    constants.INFO: 'info',
    constants.SUCCESS: 'success',
    constants.WARNING: 'warning',
    constants.ERROR: 'danger',
}
@login_required(login_url='login')
def home(request):
    #use this setting just for multiple database testing
    database=request.user.email
    settings.DATABASES[database]={
                    'ENGINE': 'django.db.backends.sqlite3',
                     'NAME': BASE_DIR / "{}.sqlite3".format(database),
                }
    print(settings.DATABASES)
    res=management.call_command('migrate', verbosity=4,interactive=False,database=database,run_syncdb=True)
    print(request.user._state.db)  #current Database name
    print(User.objects.using(database).all()) #get all users from current loggedin user database
    print(request.user._state.db)
    print(settings.DATABASES)
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


