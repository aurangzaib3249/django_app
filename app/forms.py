from dataclasses import fields
import email
from pyexpat import model
from django import forms
from .models import *
from dataclasses import field, fields
from pyexpat import model
from django import forms

from .models import User

from django.contrib.auth.forms import UserCreationForm
class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','phone','address',"password1","password2"]
        widget={
            "full_name":forms.TextInput({"class":"form-control","placeholder":"Enter Full Name"}),
            "email":forms.TextInput({"class":"form-control","placeholder":"E-mail"}),
            "phone":forms.TextInput({"class":"form-control","placeholder":"Phone Number"}),
            "password1":forms.PasswordInput({"class":"form-control","placeholder":"Password"}),
            "password2":forms.PasswordInput({"class":"form-control","placeholder":"Confirm Password"}),
            "address":forms.Textarea({"class":"form-control","placeholder":"Full adddres"}),
            
        }
        
    def clean_email(self):
        email=self.cleaned_data["email"]
        if "@" not in email:
            raise forms.ValidationError("Enter valid email")
        return email
    def clean_phone(self):
        phone=self.cleaned_data["phone"]
        if len(phone)<12:
            raise forms.ValidationError("Phone should have at least 12 letters")
        return phone
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["full_name",'email','phone','phone','address']
        
        