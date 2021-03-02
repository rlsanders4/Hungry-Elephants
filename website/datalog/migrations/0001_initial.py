# Generated by Django 3.1.6 on 2021-03-02 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FeedingData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rfid_tag_number', models.CharField(max_length=10)),
                ('unix_time', models.CharField(max_length=10)),
                ('site_code', models.CharField(max_length=3)),
                ('antenna_number', models.CharField(max_length=2)),
            ],
        ),
    ]
