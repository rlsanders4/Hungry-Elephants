# Generated by Django 3.1.5 on 2021-04-13 21:28

from django.db import migrations
from django.contrib.auth.models import User

class Migration(migrations.Migration):

    dependencies = [
        ('adminops', '0001_ACTUAL_initial'),
    ]

    def initialize_admin(apps, schema_editor):
        # create superuser with username 'admin', password 'admin'
        user = User.objects.create_superuser('admin','','admin')
        user.save()

    operations = [
        migrations.RunPython(initialize_admin),
    ]