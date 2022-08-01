from django.core import management
from django.core.management.commands import makemigrations,migrate
from django.core.management import BaseCommand



class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Run makemigrations Commands.....")
        migrations=management.call_command('makemigrations', verbosity=0, interactive=False,stdout=print())
        print("Migrations is created Now change in database",migrations)
        res=management.call_command('migrate', verbosity=0, interactive=False)
        print("Change completed",res)
        
        