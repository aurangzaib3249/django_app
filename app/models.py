from distutils.command.upload import upload
from enum import unique
from secrets import choice
import django
from django.db import models
from .managers import *
# Create your models here.
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField
from django_countries.fields import CountryField
from django.contrib.auth.models import PermissionsMixin




class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),unique=True)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    phone= models.CharField('Phone', max_length=15,null=True)
    address= models.CharField(max_length=200,null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    

    
class UserExtendsWithBase(AbstractBaseUser):
    username=None
    fist_name=models.CharField(_("First Name"),null=True,blank=True,max_length=25)
    last_name=models.CharField(_("Last Name"),null=True,blank=True,max_length=25)
    email = models.EmailField(_('E-email'),unique=True)
    phone=PhoneField(_("Phone Number"),null=True,blank=True)
    country = CountryField(blank_label='(select country)')
    avatar=models.ImageField(upload_to="avatar/",null=True,blank=True)
    is_admin=models.BooleanField(_("is Admin?"),default=False)
    is_active=models.BooleanField(_("is Active?"),default=True)
    date_joined=models.DateTimeField(_("Date Joined"),auto_now_add=True)
    last_login = models.DateTimeField(_("last login"), blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    objects=UserBaseManager()
    class Meta:
        verbose_name = _('Base User')
        verbose_name_plural = _('Base Users')
    @property
    def get_full_name(self):
        return self.fist_name+" "+self.last_name
    @property
    def get_short_name(self):
        if self.fist_name:
            return self.fist_name
        else:
            if self.last_name:
                return self.last_name
            else:
                return None
    @property
    def has_perm(self,perm,obj=None):
        return True
    @property
    def has_module_perm(self,app_label):
        return True
    @property
    def get_country(self):
        if self.country:
            if self.country=="(select country)":
                return "Country not Selected"
            else:
                return self.country
        return "Country not Selected"
    def is_staff(self):
        return self.is_staff
    @property
    def is_active(self):
        return self.is_active
    @property
    def is_first_time(self):
        if self.last_login:
            return False
        else:
            return True
    