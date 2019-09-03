from django.db import models


class Bank(models.Model):
    bank_id = models.BigIntegerField(null=False, blank = False)
    name = models.CharField(max_length=49)

