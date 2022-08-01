from django.core.management import BaseCommand
from app.models import User


class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        print("Custom Supper user creation area")
        email=input("Enter email adddress:")
        while not email:
            email=input("Enter email adddress:")
        password=input("Enter Password:")
        while not password:
            password=input("Enter password:")
        try:
            user,created=User.objects.get_or_create(email=email,is_active=True,is_superuser=True)
            if created:
                user.set_password(password)
                return "Supper user created successfully"
            else:
                return "Supper User already exist in database with this username"
        except Exception as ex:
            print(ex)
            return "Error during user creation"
        
        return 