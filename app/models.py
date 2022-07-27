from distutils.command.upload import upload
from enum import unique
from secrets import choice
from unicodedata import category
import django
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager

# Create your models here.
from django.utils.translation import gettext_lazy as _
from phone_field import PhoneField
from django_countries.fields import CountryField
from django.contrib.auth.models import PermissionsMixin
from django.utils.text import slugify
from django.db.models.signals import *


class UserManager(BaseUserManager):
   
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


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
        
    