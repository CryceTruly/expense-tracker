from django.db import models
from expense_tracker.apps.authentication.models import User

# Create your models here.

class Expense(models.Model):
    PAYMENT_OPTIONS=[
        ('VISA','VISA'),
        ('MM','MOBILE MONEY'),
        ('CASH','CASH'),

    ]
    name=models.CharField(max_length=255,db_index=True)
    spent_on=models.DateField(blank=False,null=False)
    payment_type=models.CharField(max_length=255,choices=PAYMENT_OPTIONS,null=False)
    description=models.TextField(blank=True)
    currency=models.CharField(max_length=20,default="Ugx")
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
