# Generated by Django 4.2.3 on 2023-07-09 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_facility_uid"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="hospital_name",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
