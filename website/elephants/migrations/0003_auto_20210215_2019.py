# Generated by Django 3.1.5 on 2021-02-16 02:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elephants', '0002_auto_20210215_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='max_feeds',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]