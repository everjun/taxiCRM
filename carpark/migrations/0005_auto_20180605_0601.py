# Generated by Django 2.0.5 on 2018-06-05 06:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carpark', '0004_auto_20180604_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='carpark.Car'),
        ),
    ]