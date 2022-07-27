from distutils.command.upload import upload
from enum import unique
from secrets import choice
from unicodedata import category
import django
from django.db import models
from django.dispatch import receiver
from .managers import *
# Create your models here.
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField
from django_countries.fields import CountryField
from django.contrib.auth.models import PermissionsMixin
from django.utils.text import slugify
from django.db.models.signals import *



class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'),unique=True)
    full_name = models.CharField(max_length=100,null=True,blank=True)
    phone= models.CharField('Phone', max_length=15,null=True)
    address= models.CharField(max_length=200,null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    country = CountryField(blank_label='(select country)',null=True)
    avatar=models.ImageField(upload_to="avatar/",null=True,blank=True)
    zip_code=models.CharField(max_length=10,null=True,blank=True)
    slug=models.SlugField(default=None)
    def __str__(self) -> str:
        return str(self.user)
    
    

@receiver (pre_save,sender=Profile)
def create_slug(sender,instance,**kwargs):
    instance.slug=instance.user.email
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
        
        

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
class ItemCategory(models.Model):
    category=models.CharField(max_length=20)
    def __str__(self):
        return self.category

    # pre delete functions
    def delete(self,*args, **kwargs):
        print("Delete function")
        count=Item.objects.filter(category__category=self.category).count()
        print(count)
        if count>0:
            raise ValueError(self.category+" have items in Item table please delete items before")
        else:
            super(ItemCategory,self).delete(*args, **kwargs)
    
class Item(models.Model):
    item_name=models.CharField(_("Item Name"),max_length=35)
    item_code=models.CharField(max_length=35,blank=True,null=True)
    category=models.ForeignKey(ItemCategory,on_delete=models.CASCADE)
    item_price=models.IntegerField(default=0)
    item_qty=models.IntegerField(default=0)
    item_remaining_qty=models.IntegerField(null=True,blank=True)
    slug=models.SlugField(null=True,blank=True)
    #post save override function
    def save(self,*args, **kwargs):
        super(Item,self).save(*args, **kwargs)
        if not self.item_code:
            self.item_code=self.category.category+"_"+str(self.id)
            if not self.slug:
                self.slug=slugify(self.item_code)
            self.save()
    
        
    def __str__(self) -> str:
        return self.item_code
        
    