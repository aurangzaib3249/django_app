from __future__ import unicode_literals
import re
from tkinter.messagebox import QUESTION
from unicodedata import category
from urllib import request
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_app.settings import *
from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminChangeForm
from .forms import UserForm
from .models import *
from django.contrib.auth import models as auth_models
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
# Register your models here.
from django.conf import settings

from django.contrib import messages


class UserAdmin(BaseUserAdmin):
    add_form = UserForm
    model = User
    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser   
    list_display = ('full_name','email','phone', 'is_superuser','is_active')
    list_filter = ('full_name','email','phone','is_superuser', 'is_active','date_joined')
    fieldsets = (
        (None, {'fields': ('full_name','email','phone','address','is_superuser', 'last_login',"date_joined")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email','phone','address', 'password1', 'password2', 'is_staff', 'is_active', 'last_login',"date_joined")}
        ),
    )
    def set_in_active(UserAdmin,request, queryset):
        queryset.update(is_active = 0)
        messages.success(request, "Selected Users Marked as Inactive Successfully !!")
    def set_active(UserAdmin,request, queryset):
        queryset.update(is_active = 1)
        messages.success(request, "Selected Users Marked as Inactive Successfully !!")
    admin.site.add_action(set_in_active, "Make Active")
    admin.site.add_action(set_active, "Make Inactive")
    search_fields = ('email',)
    ordering = ('email',)
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)


class ItemAdmin(admin.ModelAdmin):
    model=Item
    readonly_fields=("date",)
    list_display=("item_code","item_name","category","item_price","is_active")
    list_filter=("is_active","category")
    fieldsets=(
        ("Item Category",{"fields":("category",)}),
        
        ("Item Details",{"fields":("item_name","item_price","item_discounted_price","item_qty","item_remaining_qty")}),
        ("Status",{"fields":("is_active",)}),
        
        ("Disabled Fields",{"fields":("item_code","slug","date")}),
    )
    add_fieldsets=(
        (None,{
            "classes":("wide",),
            "fields":("category","item_name","item_price","item_discounted_price","item_qty","item_remaining_qty","date","is_active")
        })
    )
    createonly_fields = ["item_code","slug" ]
    def save_model(self, request, obj, form, change):
        obj.save(using=request.user.email)
    def delete_model(self, request, obj):
        obj.delete(using=request.user.email)
    def get_queryset(self, request):
        return super().get_queryset(request).using(request.user.email)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=request.user.email, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=request.user.email, **kwargs)
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(ItemAdmin, self).get_readonly_fields(request, obj))
        createonly_fields = list(getattr(self, 'createonly_fields', []))
        if obj:  
            readonly_fields.extend(createonly_fields)
        return readonly_fields
    ordering=("item_code",)
    search_fields=("item_code",)
    def get_inline_instances(self, request,obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
    
    def get_queryset(self, request):
        r=super(ItemAdmin,self).get_queryset(request)
        if request.user.is_superuser:
            return r
        return r.using(request.user.email).filter(category__user=request.user)
    def save_model(self, request, obj, form, change):
        obj.save(using=request.user.email)
    def delete_model(self, request, obj):
        obj.delete(using=request.user.email)
    def get_queryset(self, request):
        return super().get_queryset(request).using(request.user.email)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=request.user.email, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=request.user.email, **kwargs)
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super(ItemAdmin, self).get_readonly_fields(request, obj))
        createonly_fields = list(getattr(self, 'createonly_fields', []))
        if obj:  
            readonly_fields.extend(createonly_fields)
        return readonly_fields
    """def get_form(self, request, obj, **kwargs):
        form = super(ItemAdmin,self).get_form(request, obj, **kwargs)
        form.base_fields['category'] = forms.ModelChoiceField(queryset=ItemCategory.objects.filter(user=request.user))
        return form"""
class CategoryAdmin(admin.ModelAdmin):
    model=ItemCategory
    list_display=("category",)
    list_filter=("category",)
    fieldsets=(
        
        ("Category",{"fields":("category",)}),
    )
    add_fields=(
        (None,{
            "classes":("wide",),
            "fields":("category",)
        })
    )
    """def get_form(self, request, obj, **kwargs):
        form = super(CategoryAdmin,self).get_form(request, obj, **kwargs)
        form.base_fields['user'] = forms.CharField(initial=request.user,disabled=True,help_text="You cannot edit this field")
        return form"""
    def save_model(self, request, obj, form, change):
        obj.save(using=request.user.email)
    def delete_model(self, request, obj):
        obj.delete(using=request.user.email)
    def get_queryset(self, request):
        print(settings.DATABASES)
        return super().get_queryset(request).using(request.user.email)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=request.user.email, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=request.user.email, **kwargs)
    ordering=("category",)
    search_fields=("category",)
admin.site.register(User, UserAdmin)
admin.site.register(Item,ItemAdmin)
admin.site.register(ItemCategory,CategoryAdmin)
