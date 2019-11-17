from rest_framework import serializers
from .models import Expense
import datetime

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields=['id','name','amount','spent_on','description','currency',"category"]
    def create(self,data):
        self.validate(data)
        return data
    def validate(self,data):
        if(data['spent_on']>datetime.date.today()):
            raise serializers.ValidationError({'spent_on':'Invalid date,date must be prior or today'})
        return data
