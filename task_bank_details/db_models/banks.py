from django.db import models


class Bank(models.Model):
    bank_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=49)

    class Meta:
        unique_together = ['bank_id', 'name']

