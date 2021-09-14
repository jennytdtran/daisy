# Generated by Django 2.2.20 on 2021-07-13 11:25

import core.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20210622_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='access',
            name='contact',
            field=models.ForeignKey(blank=True, help_text='Use either `contact` or `user`', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Contact', verbose_name='Contact that has the access'),
        ),
        migrations.AddField(
            model_name='access',
            name='created_by',
            field=models.ForeignKey(blank=True, help_text='Which User added this entry to DAISY', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='access',
            name='user',
            field=models.ForeignKey(blank=True, help_text='Use either `contact` or `user`', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='User that has the access'),
        ),
        migrations.AddField(
            model_name='access',
            name='was_generated_automatically',
            field=models.BooleanField(default=False, help_text='Was the entry generated automatically, e.g. by REMS?', verbose_name='Was created automatically'),
        ),
        migrations.AddField(
            model_name='contact',
            name='oidc_id',
            field=models.CharField(blank=True, help_text="Internal user identifier from OIDC's IdP", max_length=64, null=True, unique=True, verbose_name='OIDC user identifier'),
        ),
        migrations.AddField(
            model_name='user',
            name='api_key',
            field=models.CharField(default=core.models.user.create_api_key, help_text='A token used to authenticate the user for accessing API', max_length=64, verbose_name='API key'),
        ),
        migrations.AddField(
            model_name='user',
            name='oidc_id',
            field=models.CharField(blank=True, help_text="Internal user identifier coming from OIDC's IdP", max_length=64, null=True, unique=True, verbose_name='OIDC user identifier'),
        ),
        migrations.AlterField(
            model_name='access',
            name='defined_on_locations',
            field=models.ManyToManyField(blank=True, help_text='The dataset locations on which access is defined.', related_name='accesses', to='core.DataLocation', verbose_name='Data Locations'),
        ),
        migrations.AddConstraint(
            model_name='access',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('user__isnull', False), ('contact__isnull', True)), models.Q(('user__isnull', True), ('contact__isnull', False)), models.Q(('user__isnull', True), ('contact__isnull', True)), _connector='OR'), name='user_or_contact_only'),
        ),
    ]