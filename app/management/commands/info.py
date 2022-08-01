from django.core.management import BaseCommand



class Command(BaseCommand):
    help="This command show website information just type python manage.py info"
    
    def handle( self,*args, **kwargs ):
      
    
        return "Django App for practice"