from django.contrib import admin
from .models import Expense
# Register your models here.


admin.sites.register(Expense)