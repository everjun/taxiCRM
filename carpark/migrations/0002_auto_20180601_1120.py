# Generated by Django 2.0.5 on 2018-06-01 11:20

import carpark.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpark', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, validators=[carpark.models.is_driver_validator]),
        ),
    ]