from __future__ import unicode_literals
from urllib import request
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
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
LIST_DISPLAY_FOR_SUPERUSER=('full_name','email','phone', 'is_superuser','is_active')
LIST_FILTER_FOR_SUPERUSER=('full_name','email','phone','is_superuser', 'is_active','date_joined')
FIELDSSETS_FOR_SUPERUSER=(
        (None, {'fields': ('full_name','email','phone','address','is_superuser', 'last_login',"date_joined","is_access")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
ADD_FIELDSSETS_FORSUPERUSER=(
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email','phone','address', 'password1', 'password2', 'is_staff', 'is_active', 'last_login',"date_joined")}
        ),
    )
SEARCH_FIELDS_FORSUPERUSER=('email',)
ORDERING_FOR_SUPERUSER=('email',)
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
        (None, {'fields': ('full_name','email','phone','address','is_superuser', 'last_login',"date_joined","is_access")}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('full_name','email','phone','address', 'password1', 'password2', 'is_staff', 'is_active', 'last_login',"date_joined")}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields=["slug","item_code"]
    def get_queryset(self, request):
        qs = super(ItemAdmin, self).get_queryset(request)
        if request.user.is_superuser: #remove this line if you want to show only user items also remove return qs
            return qs
        return qs.filter(category__user=request.user)
    def get_form(self, request, obj, **kwargs):
        form = super(ItemAdmin,self).get_form(request, obj, **kwargs)
        form.base_fields['category'] = forms.ModelChoiceField(queryset=ItemCategory.objects.filter(user=request.user))
        return form
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display=["category","user"]
    def get_queryset(self, request):
        qs = super(ItemCategoryAdmin, self).get_queryset(request)
        if request.user.is_superuser: #remove this line if you want to show only user items also remove return qs
            return qs
        return qs.filter(user__id=request.user.id)
    def get_form(self, request, obj, **kwargs):
        form = super(ItemCategoryAdmin,self).get_form(request, obj, **kwargs)
        form.base_fields['user'] = forms.ModelChoiceField(queryset=User.objects.filter(id=request.user.id))
        return form
admin.site.register(User, UserAdmin)
admin.site.register(ItemCategory,ItemCategoryAdmin)
admin.site.register(Item,ItemAdmin)
