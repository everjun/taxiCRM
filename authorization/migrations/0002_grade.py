# Generated by Django 2.0.5 on 2018-06-06 04:58

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5)])),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_as_client', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_as_driver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
