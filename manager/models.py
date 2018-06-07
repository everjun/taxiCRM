from django.db import models

# Create your models here.
class PriceRule(models.Model):
    price_for_sit = models.DecimalField(max_digits=7, decimal_places=2)
    price_for_km = models.DecimalField(max_digits=7, decimal_places=2)