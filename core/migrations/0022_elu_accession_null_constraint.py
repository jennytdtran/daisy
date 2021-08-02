# Generated by Django 2.2.24 on 2021-07-29 10:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20210720_1721'),
    ]
    
    def set_empty_elu_accession_to_null(apps, schema_editor):
        classes_to_update = ['Cohort', 'Dataset', 'Partner', 'Project']
        for class_to_update in classes_to_update:
            model_to_update = apps.get_model('core', class_to_update)
            for obj in model_to_update.objects.all():
                if obj.elu_accession == '' or obj.elu_accession == '-':
                    obj.elu_accession = None
                    obj.save()

    operations = [
        migrations.AlterField(
            model_name='cohort',
            name='elu_accession',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='elu_accession',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='elu_accession',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='elu_accession',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.RunPython(set_empty_elu_accession_to_null),
    ]
