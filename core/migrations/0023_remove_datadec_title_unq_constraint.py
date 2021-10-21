# Generated by Django 2.2.24 on 2021-07-28 20:59

import core.models.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_elu_accession_null_constraint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datadeclaration',
            name='title',
            field=core.models.utils.TextFieldWithInputWidget(help_text='Title is a brief description for the  data declaration. Think of how you - in the lab - refer to  data from a particular source; use that as the title.', max_length=255, verbose_name='Title'),
        ),
        migrations.AddConstraint(
            model_name='datadeclaration',
            constraint=models.UniqueConstraint(fields=('title', 'dataset'), name='unique_title_dataset'),
        ),
    ]
