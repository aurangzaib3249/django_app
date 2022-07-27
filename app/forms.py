from dataclasses import fields
import email
from pyexpat import model
from django import forms
from .models import *
from dataclasses import field, fields
from pyexpat import model
from django import forms

from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,AuthenticationForm
class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=("email",)
        
class ChanageUsersFrom(UserChangeForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','address']
        help_texts = {
            'password ': _(''),
        }

        exclude = ('password',)

        
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','phone','address']
        
        