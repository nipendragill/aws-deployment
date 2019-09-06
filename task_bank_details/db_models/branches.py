from django.db import models
from .banks import Bank


class Branches(models.Model):
    ifsc_code = models.CharField(max_length=11, unique=True)
    bank_id = models.ForeignKey(Bank, on_delete=models.PROTECT)
    branch = models.CharField(max_length=74)
    address = models.CharField(max_length=195)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=26)
