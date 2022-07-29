from datetime import datetime
from unicodedata import category
from venv import create
from django.forms import PasswordInput
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.messages import constants 
from django.contrib import messages
import timeit

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

def queries(request):
    
    return render(request,"queries.html")

@require_http_methods(["GET","POST"])
def create_query(request):
    if request.method=="POST":
        name=request.POST.get("name")
        if name:
            flag=ItemCategory.objects.create(category=name,user=request.user)
            if flag:
                messages.success(request,"Item Category is created")
            else:
                messages.success(request,"Error")
    return render(request,"queries.html")

@require_http_methods(["GET","POST"])
def get_or_create_query(request):
    if request.method=="POST":
        name=request.POST.get("name")
        if name:
            flag,created=ItemCategory.objects.get_or_create(category=name,user=request.user)
            if created:
                messages.success(request,"Item Category is created")
            else:
                messages.success(request,"Item Category already exist")
            print(flag)
    return render(request,"queries.html")
@require_http_methods(["GET","POST"])
def update_or_create_query(request):
    if request.method=="POST":
        name=request.POST.get("name")
        if name:
            flag,obj=ItemCategory.objects.update_or_create(category=name.upper(),user=request.user,defaults={"category":name.upper()})
            print(flag,obj)
            if obj:
                messages.success(request,"Item Category is created")    
            else:
                messages.success(request,"Item Category is updated")
                
    return render(request,"queries.html")

@require_http_methods(["GET","POST"])
def bulk_create_query(request):
    if request.method=="POST":
        name=request.POST.get("name")
        num=request.POST.get("number")
        if num:
            num=int(num)
        else:
            num=0
        objs=[]
        for i in range(0,num):
            objs.append(ItemCategory(category=name+"_"+str(i),user=request.user))
        flag,obj=ItemCategory.objects.update_or_create(category=name.upper(),user=request.user,defaults={"category":name.upper()})
        print(flag,obj)
        flag=ItemCategory.objects.bulk_create(objs)
        if flag:
            messages.success(request,str(num)+" Items Category is created")    
        else:
            messages.success(request,"Error")
                
    return render(request,"queries.html")
@require_http_methods(["GET","POST"])
def bulk_update_query(request):
    obj=ItemCategory.objects.all()
    for ob in obj:
        ob.category= ob.category.upper()
    flag=ItemCategory.objects.bulk_update(obj,["category"])
    print(flag)    
    return render(request,"queries.html")

def select_related_query(request):
    # using select related method
    start = timeit.default_timer()
    obj=ItemCategory.objects.select_related("user")
    stop = timeit.default_timer()
    for i in obj:
        print(i.user.email)
    t1=stop - start
    print('Time: ', t1)
    #using all method
    print("Select Related End")
    start = timeit.default_timer()
    obj=ItemCategory.objects.all()
    for i in obj:
        print(i.user.email)
    stop = timeit.default_timer()
    t2=stop - start
    print('Time: ', t2)   
    t3= t2-t1
    print('diff: ', t3)    
    return render(request,"queries.html",{"time":t3})

def prefetch_related_query(request):
    # using prefetch related method
    start = timeit.default_timer()
    obj=Order.objects.select_related("user").prefetch_related("OrderItems")
    stop = timeit.default_timer()
    for i in obj:
        print(i.user.email)
    t1=stop - start
    print('Time: ', t1)
    #using all method
    print("Select Related End")
    start = timeit.default_timer()
    obj=Order.objects.all()
    for i in obj:
        for j in i.OrderItems.all():
            print(j.price)
        print(i.user.email)
    stop = timeit.default_timer()
    t2=stop - start
    print('Time: ', t2)   
    t3= t2-t1
    print('diff: ', t3)    
    return render(request,"queries.html",{"time1":t3})