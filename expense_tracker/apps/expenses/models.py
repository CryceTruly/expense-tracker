from django.db import models
from expense_tracker.apps.authentication.models import User


class Expense(models.Model):

    CATEGORY_OPTIONS=[
        ('ONLINE_SERVICES','ONLINE_SERVICES'),
        ('RENT','RENT'),
        ('BUSINESS_MISCELLENOUS','BUSINESS_MISCELLENOUS'),
        ('TRAVEL','TRAVEL'),
        ('GENERAL_MERCHANDISE','GENERAL_MERCHANDISE'),
        ('RESTUARANTS','ENTERTAINMENT'),
        ('GASOLINE_FUEL','GASOLINE_FUEL'),
        ('INSURANCE','INSURANCE'),
        ('OTHERS','OTHERS')
    ]
    name=models.CharField(max_length=255,db_index=True)
    spent_on=models.DateField(blank=False,null=False)
    description=models.TextField(blank=True)
    currency=models.CharField(max_length=20,default="Ugx")
    category=models.CharField(max_length=200,choices=CATEGORY_OPTIONS,null=False,blank=False)
    owner=models.ForeignKey(to=User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
