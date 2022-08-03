from django.core.management import BaseCommand
from app.models import *
from datetime import datetime
from pytz import timezone as tz
import pytz
import string   
from django.utils import timezone as dtz
import random
date_format='%m/%d/%Y %H:%M:%S %Z'
class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        records=100
        domain="@gmail.com"
        password="adminasdfghjqweq"
        
        for i in range(records):
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))    
            email="{}{}".format(ran,domain)
            user=User.objects.create(email=email)
            user.set_password(password)
            user.save()
            print(email," User is created")
        for i in range(records):
            obj=DateTime.objects.create()
        return 
    
    def get_pst_time(self):
        
       

        date_format='%m/%d/%Y %H:%M:%S'
        date1 = datetime.now()
        print(date1)
        #date.strftime(date_format)

        date = date1.astimezone(tz('US/Pacific'))
        print(date)
        #date.strftime(date_format)
        return date
