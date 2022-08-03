from secrets import choice
import django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager
# Create your models here.
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as dtz
from pytz import timezone as tz
from datetime import datetime
date_format='%Y-%m-%d %H:%M:%S'
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
    
choices=(
    ("PST","PST"),
    ("UTC","UTC")
)
choices1=(
    ("PST-UTC","PST-UTC"),
    ("UTC-PST","UTC-PST")
)
class DateTime(models.Model):
    date_time=models.DateTimeField(default=dtz.now) # django save acutal value in field but in display django always show date time in utc i also change timezone in setting but still same thats why i used CharField for date time
    date_char=models.CharField(default=dtz.now().astimezone(tz('US/Pacific')).strftime(date_format),max_length=150) # django save acutal value in field but in display django always show date time in utc i also change timezone in setting but still same thats why i used CharField for date time
    status=models.CharField(choices=choices,default="PST",max_length=20)
    
    
    def __str__(self) -> str:
        return "Time :{} and Status is {}".format(self.date_char,self.status)
    
class Tracker(models.Model):
    track=models.CharField(max_length=20,choices=choices1,default="PST-UTC")
    def __str__(self) -> str:
        return self.track