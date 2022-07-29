from secrets import choice
import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager
# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from django.utils import timezone
from django.core.exceptions import ValidationError
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
    
    
class ItemCategory(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    category=models.CharField(max_length=20)
    def __str__(self):
        return self.category
     #model Level validation 
    def delete(self,*args, **kwargs):
        count=Item.objects.filter(category__category=self.category).count()
        print(count)
        if count>0:
            raise ValidationError(self.category+" have items in Item table please delete items before")
        else:
            super(ItemCategory,self).delete(*args, **kwargs)
    
class Item(models.Model):
    item_name=models.CharField(_("Item Name"),max_length=35)
    item_code=models.CharField(max_length=35,blank=True,null=True)
    category=models.ForeignKey(ItemCategory,on_delete=models.CASCADE)
    item_price=models.IntegerField(default=0)
    item_discounted_price=models.IntegerField(blank=True,null=True)
    item_qty=models.IntegerField(default=0)
    item_remaining_qty=models.IntegerField(null=True,blank=True)
    slug=models.SlugField(null=True,blank=True)
    is_active=models.BooleanField(default=True)
    date=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    #model Level validation 
    def clean(self):
        if not self.item_remaining_qty:
            raise ValidationError({"item_remaining_qty":"Please enter Item remaining Quantity"})
        if not self.item_name:
            raise ValidationError({"item_name":"Please enter Item Name"})
        if self.item_discounted_price:
            if self.item_discounted_price>=self.item_price:
                raise ValidationError({"item_discounted_price":"Discounted Price must be less than the Item sale price"})
    @property
    def get_item_price(self):
        if self.item_discounted_price:
            return self.item_discounted_price
        else:
            return self.item_price
    @property
    def is_available(self):
        if self.item_remaining_qty >0:
            return True
        else:
            return False
    @property
    def get_item_remianing_qty(self):
        return self.item_remaining_qty
    def save(self,*args, **kwargs):
        self.full_clean()
        super(Item,self).save(*args, **kwargs)
        if not self.item_code:
            self.item_code=self.category.category+"_"+str(self.id)
            if not self.slug:
                self.slug=slugify(self.item_code)
            self.save()
    def __str__(self) -> str:
        return self.item_code
    

    
class OrderItem(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    qty=models.IntegerField(default=1)
    price=models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return self.item.item_name+str(self.price)
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    amount=models.IntegerField(default=0)
    OrderItems=models.ManyToManyField(OrderItem)
    def __str__(self) -> str:
        return self.user.email+"_"+str(self.amount)