# Generated by Django 2.0.5 on 2018-06-05 06:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpark', '0005_auto_20180605_0601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
