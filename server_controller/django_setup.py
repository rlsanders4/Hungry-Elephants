#
# Django setup script for initializing django's ORM for the server controller.
# Connects to the database and the installed apps in the adjacent 'website' folder.
# The server controller scripts access the website's packages relatively, so this
# script MUST BE HERE in 'Hungry-Elephants/server_controller/' to work.
#
import django
from django.conf import settings
from pathlib import Path
import sys
# Get the path to 'Hungry-Elephants/website/' where the django project, apps, and models are.
path = str(Path(__file__).resolve().parent.parent/ 'website')
# Add the django project to python's list of import-resolving paths, 
# allowing python to find and import apps and models from the 'website' folder.
# This is kind of a hack/workaround, but it facilitates the project folder structure we desire.
# It would be undesireable to put these scripts in the 'website' folder or to use the package
# manager for such volatile packages.
sys.path.append(path)

def initDjango():
    # Get the base django project directory again
    BASE_DIR = Path(__file__).resolve().parent.parent / 'website'

    settings.configure(
        BASE_DIR = BASE_DIR,
        # configure DB
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        },
        # Keep this up-to-date; any model we want to access from the server controller must have
        # its parent app referenced here
        INSTALLED_APPS=[
            'elephants.apps.ElephantsConfig',
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'adminops.apps.AdminopsConfig',
        ]
    )
    django.setup()