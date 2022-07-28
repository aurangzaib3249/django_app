from django.db import models
from django.contrib.auth.models import AbstractBaseUser,AbstractUser,BaseUserManager


class ItemQuerySet(models.QuerySet):
    def get_active_items(self):
        return self.filter(is_active=True).all()
    def get_inactive_items(self):
        return self.filter(is_active=False).all()
    def get_user_active_items(self,user):
        return self.filter(category__user=user,is_active=True).all()
    def get_user_inactive_items(self,user):
        return self.filter(category__user=user,is_active=False).all()
    def get_user_all_items(self,user):
        return self.filter(category__user=user).all()
    
class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model,using=self._db)
    
    def get_active_all_items(self):
        return self.get_queryset().get_active_items()
    def get_inactive_all_items(self):
        return self.get_queryset().get_inactive_items()
    def get_user_active_items(self,user):
        return self.get_queryset().get_user_active_items(user)
    def get_user_inactive_items(self,user):
        return self.get_queryset().get_user_inactive_items(user)
    def get_user_all_items(self,user):
        return self.get_queryset().get_user_all_items(user)
    
class UserManager(BaseUserManager):
    
    def create_user(self,email,password,**extrax_fields):
        if not email:
            raise ValueError("You must have an email!!!")
        if not password:
            raise ValueError("You must have password")
        email=self.normalize_email(email)
        user=self.model(email=email,**extrax_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)