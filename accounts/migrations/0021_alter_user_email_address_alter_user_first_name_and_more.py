# Generated by Django 4.2.3 on 2023-07-17 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0020_emergency_paramedic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email_address",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="location",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="phone_number",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="state",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
