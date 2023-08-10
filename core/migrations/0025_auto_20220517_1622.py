# Generated by Django 2.2.25 on 2022-05-17 14:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0024_auto_20211004_1610"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="domain_type",
            field=models.TextField(
                choices=[
                    ("not_specified", "Not Specified"),
                    ("agreement", "Agreement"),
                    ("ethics_approval", "Ethics Approval"),
                    ("consent_form", "Consent Form"),
                    ("subject_information_sheet", "Subject Information Sheet"),
                    ("project_proposal", "Project Proposal"),
                    (
                        "data_protection_impact_assessment",
                        "Data Protection Impact Assessment",
                    ),
                    ("other", "Other"),
                ],
                default="not_specified",
                verbose_name="Domain Type",
            ),
        ),
        migrations.AlterField(
            model_name="userestriction",
            name="use_restriction_rule",
            field=models.TextField(
                choices=[
                    ("PROHIBITION", "PROHIBITION"),
                    ("OBLIGATION", "OBLIGATION"),
                    ("PERMISSION", "PERMISSION"),
                    ("CONSTRAINED_PERMISSION", "CONSTRAINED_PERMISSION"),
                ],
                default="PROHIBITION",
                max_length=64,
                verbose_name="Use Restriction Rule",
            ),
        ),
    ]
