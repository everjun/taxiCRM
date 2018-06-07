import datetime


from django.core.validators import RegexValidator
from django.contrib.auth.models import User, Group
from django.db import models
from django.core.exceptions import ValidationError


def is_driver_validator(user):
    user = User.objects.get(id=user)
    g = Group.objects.get(name="Driver")
    if g not in user.groups.all():
        raise ValidationError("user is not a driver")

# Create your models here.
class Car(models.Model):
    number = models.CharField(max_length=9, 
                              validators=[RegexValidator(regex=r"^[АВЕКМНОРСТУХ][0-9]{3}[АВЕКМНОРСТУХ]{2}[0-9]{0,3}")])
    driver = models.OneToOneField(User, on_delete=models.CASCADE, validators=[is_driver_validator])
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=30)
    color = models.CharField(max_length=20)

    def __str__(self):
        return "%s %s - %s" % (self.brand, self.model, self.number)


class Point(models.Model):
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)


class Trip(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    startpoint = models.TextField()
    startpoint_coordinate = models.ForeignKey(Point, on_delete=models.CASCADE, related_name="strt_crd")
    endpoint = models.TextField()
    endpoint_coordinate = models.ForeignKey(Point, on_delete=models.CASCADE, related_name="end_crd")
    create_time = models.DateTimeField(default=datetime.datetime.now)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def is_done(self):
        return True if self.end_time else False

    def __str__(self):
        return "%s - %s - %s" % (self.startpoint, self.endpoint, "Done" if self.is_done() else "In process")


