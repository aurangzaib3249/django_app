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
    readonly_fields=("last_login","date_joined",'is_superuser',)
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

class ItemFilterByDiscountedPrice(admin.SimpleListFilter):
    title="Price"
    parameter_name = 'item_discounted_price'

    def lookups(self, request,model_admin):
        return (
            ("Discount Items","Discount Items"),
            ("Non Discount Items","Non Discount Items")
        )
    def queryset(self, request,queryset):
        if not self.value():
            return queryset
        if self.value()=="Discount Items":
            return queryset.filter(item_discounted_price__isnull=True)
        if self.value()=="Non Discount Items":
            return queryset.filter(item_discounted_price__isnull=False)
class ItemFilterByUpdated(admin.SimpleListFilter):
    title="Update Status"
    parameter_name = 'updated_at'
    def lookups(self, request,model_admin):
        return (
            ("Updated Items","Updated Items"),
            ("Non Updated Items","Non Updated Items")
        )
    def queryset(self, request,queryset):
        if not self.value():
            return queryset
        if self.value()=="Updated Items":
            return queryset.filter(updated_at__isnull=True)
        if self.value()=="Non Updated Items":
            return queryset.filter(updated_at__isnull=False)
class ItemFilterStatus(admin.SimpleListFilter):
    title="Available Status"
    parameter_name = 'is_available'

    def lookups(self, request,model_admin):
        return (
            ("Available","Available"),
            ("Not Available","Not Available")
        )
    def queryset(self, request,queryset):
        if not self.value():
            return queryset
        if self.value()=="Available":
            return queryset.filter(item_remaining_qty__gt=0)
        if self.value()=="Not Available":
            return queryset.filter(item_remaining_qty__lte=0)
class ItemFilterCategory(admin.SimpleListFilter):
    title="Categories"
    parameter_name = 'category'
    def lookups(self, request,model_admin):
        types = set([t.category for t in ItemCategory.objects.all().distinct()])
        tup=zip(types, types) 
        print(tup)
        return  tup   
    def queryset(self, request,queryset):
        if not self.value():
            return queryset
        if self.value():
            return queryset.filter(category__category=self.value())
        
    
        
class ItemAdmin(admin.ModelAdmin):
    model=Item
    
    readonly_fields=("item_code","slug")
    list_display=("id","item_code","item_name","category","get_item_price","item_remaining_qty","is_available","is_active")
    list_filter=("is_active","created_at",ItemFilterCategory,ItemFilterByDiscountedPrice,ItemFilterByUpdated)
    fieldsets=(
        ("Item Details",{"fields":("item_name","category","item_price","item_discounted_price","item_qty","item_remaining_qty","is_active",)}),
        ("Read only Fields",{"fields":("item_code","slug")}),
    )
    add_fieldsets=(
        (None,{
            "classes":("wide",),
            "fields":("item_code","item_name","category","item_price","item_discounted_price","item_qty","item_remaining_qty","is_active")
        })
    )
    search_fields=("item_name",)
    ordering=("-id",)
    autocomplete_fields=("category",)
    def get_inline_instances(self, request,obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)
    
class CategoryAdmin(admin.ModelAdmin):
    search_fields=("category",)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemCategory,CategoryAdmin)
admin.site.register(User, UserAdmin)
