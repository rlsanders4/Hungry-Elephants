#
# Django setup script for initializing django's ORM for the server controller TESTS.
# Connects to the database and the installed apps in the adjacent 'website' folder.
# The server controller scripts access the website's packages relatively, so this
# script MUST BE HERE in 'Hungry-Elephants/server_controller/tests' to work.
#
import django
from django.conf import settings
from pathlib import Path
import sys
from shutil import copyfile
# Get the path to 'Hungry-Elephants/website/' where the django project, apps, and models are.
path = str(Path(__file__).resolve().parent.parent.parent / 'website')
# Add the django project to python's list of import-resolving paths, 
# allowing python to find and import apps and models from the 'website' folder.
# This is kind of a hack/workaround, but it facilitates the project folder structure we desire.
# It would be undesireable to put these scripts in the 'website' folder or to use the package
sys.path.append(path)
# Get the path to the server_controller
path2 = str(Path(__file__).resolve().parent.parent.parent / 'server_controller')
sys.path.append(path2)


def initDjangoTest():
    # Get the base django project directory again
    BASE_DIR = Path(__file__).resolve().parent.parent.parent / 'website'
    # Get the directory of the test database
    DB_DIR = Path(__file__).resolve().parent.parent.parent / 'server_controller' / 'tests'

    # Get the path to the prod DB
    pathPDB = str(Path(__file__).resolve().parent.parent.parent / 'website'/ 'db.sqlite3')
    pathTDB = str(Path(__file__).resolve().parent.parent.parent / 'server_controller' / 'tests' / 'db.sqlite3')
    # copy prob DB to test environment
    try:
        copyfile(pathPDB,pathTDB)
    except:
        print("ERROR: unable to build test DB")

    settings.configure(
        BASE_DIR = BASE_DIR,
        # configure DB
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': DB_DIR / 'db.sqlite3',
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
            'datalog.apps.DatalogConfig',
        ]
    )
    django.setup()