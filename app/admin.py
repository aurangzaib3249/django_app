from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


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
class UserAdmin(BaseUserAdmin):
    add_form = UserForm
    model = User
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
    search_fields = ('email',)
    ordering = ('email',)
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User, UserAdmin)
