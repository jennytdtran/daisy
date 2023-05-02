# Generated by Django 3.2.18 on 2023-05-02 11:44

import core.models.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_permissions_data_migration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Endpoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(help_text='* Please specify the name of the endpoint', max_length=128, unique=True, verbose_name='Name')),
                ('url_pattern', models.CharField(blank=True, help_text='\n        Please specify the url pattern to the entity page and incorporate entity_id like the example:\n        <h3>https://datacatalog.elixir-luxembourg.org/e/dataset/${entity_id}</h3>', max_length=256, verbose_name='URL Pattern')),
                ('api_key', core.models.utils.HashedField(help_text="\n        * Please specify the API key to the endpoint, \n        head <a href='https://generate-random.org/api-key-generator?count=1&length=64&type=mixed-numbers&prefix=' target='_blank'> here </a> \n        to generate a random key and keep it somewhere, we only store a hash.\n        ", max_length=128, verbose_name='API Key')),
            ],
            options={
                'ordering': ['name'],
                'get_latest_by': 'added',
            },
        ),
        migrations.CreateModel(
            name='Exposure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('form_id', models.IntegerField()),
                ('created_by', models.ForeignKey(help_text='Which User added this entry to DAISY', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Created by')),
                ('dataset', models.ForeignKey(help_text='The dataset that is exposed.', on_delete=django.db.models.deletion.CASCADE, related_name='exposures', to='core.dataset', verbose_name='Dataset')),
                ('endpoint', models.ForeignKey(help_text='The endpoint to which the entity is exposed.', on_delete=django.db.models.deletion.CASCADE, related_name='exposures', to='core.endpoint', verbose_name='Endpoint')),
            ],
            options={
                'ordering': ['added'],
                'get_latest_by': 'added',
            },
        ),
    ]
