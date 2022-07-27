from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import *
from django.contrib.auth import models as auth_models
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

# Register your models here.
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form=UserChangeForm
    model = User
    list_display = ('full_name','email','phone', 'is_superuser','is_active')
    list_filter = ('email','is_superuser', 'is_active')
    fieldsets=(
        ("Required Fileds",{"fields":('email','phone',"password")}),
        ("Non Required Fields",{"fields":('full_name','address')}),
        ("Permissions",{"fields":('is_staff', 'is_active','is_superuser')}),
    )
    add_fieldsets = (
        ("Create Account", {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(UserAdmin, self).get_inline_instances(request, obj)

admin.site.register(User,UserAdmin)
admin.site.register(UserExtendsWithBase)
admin.site.register(ItemCategory)
class ItemAdmin(admin.ModelAdmin):
    
    readonly_fields=('item_code','slug' )
admin.site.register(Item,ItemAdmin)
admin.site.register(Profile)
