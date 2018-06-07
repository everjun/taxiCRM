from django.contrib.auth.models import Group, User
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            group = Group.objects.get(name="Client")
            instance.groups.add(group)
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
        

class Grade(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grade_as_client")
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="grade_as_driver")
    value = models.PositiveSmallIntegerField(validators=[MaxValueValidator(5)])