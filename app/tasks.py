from django_cron import CronJobBase, Schedule
import logging
logger=logging.getLogger(__name__)
from app.models import *
from app.models import *
from datetime import datetime
from pytz import timezone as tz
from django.utils import timezone as dtz
import pytz
from celery import shared_task
date_format='%Y-%m-%d %H:%M:%S'
flag=False


@shared_task()
def update_time_zone():
    tracker,created=Tracker.objects.get_or_create(id=1)
    print("tracker",tracker)
    if tracker.track=="PST-UTC":
        dates=DateTime.objects.filter(status="PST")
        if dates.count()<=10:
            tracker.track="UTC-PST"
            tracker.save()
        for obj in dates[:10]:
            print(obj.date_char)
            date=datetime.strptime(obj.date_char,date_format)
            date = date.astimezone(tz('UTC'))
            obj.date_time=date
            obj.date_char=date
            
            obj.status="UTC"
            obj.save()
            print(obj.date_char)
            print(date)
            
    else:
        print("Convert PST-UTC")
        dates=DateTime.objects.filter(status="UTC")
        print(dates.count())
        if dates.count()<=10:
            tracker.track="PST-UTC"
            tracker.save()
        for obj in dates[:10]:
            date=datetime.strptime(obj.date_char,date_format)
            date = date.astimezone(tz('US/Pacific'))
            obj.date_time=date
            obj.date_char=date
            obj.status="PST"
            obj.save()
