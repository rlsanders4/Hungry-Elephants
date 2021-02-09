from django.db import migrations
def combine_names(apps, schema_editor):

   # Feedingdata = apps.get_model('AppName', 'data')
   #     for data in Feedingdata.objects.all():
   #         data.name = '%s %s' % (data.???, data.???)
   #         data.save()

class Migration(migrations.Migration):

    dependencies = [
       # ('AppName', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(combine_names),
    ]