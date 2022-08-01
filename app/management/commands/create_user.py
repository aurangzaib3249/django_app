from django.core.management import BaseCommand

from app.models import User

class Command(BaseCommand):
    help="Create user with user name and password"
    
    def add_arguments(self, parser):
        parser.add_argument("-u","--user",type=str,help="Enter User name")
        parser.add_argument("-p","--password",type=str,help="Enter password")
        
    
    def handle(self,*args, **kwargs):
        print(kwargs)
        user=kwargs["user"]
        password=kwargs["password"]
        try:
            user,created=User.objects.get_or_create(email=user)
            if created:
                user.set_password(password)
                return "user created successfully"
            else:
                return "User already exist in database with this username"
        except Exception as ex:
            print(ex)
            return "Error during user creation"
        