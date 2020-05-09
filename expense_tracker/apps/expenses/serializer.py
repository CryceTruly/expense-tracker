from rest_framework import serializers
from .models import Expense
import datetime


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'date',
                  'description', "category"]

    def create(self, data):
        self.validate(data)
        return Expense.objects.create(**data)

    def validate(self, data):
        if(data['date'] > datetime.date.today()):
            raise serializers.ValidationError(
                {'date': 'Invalid date,date must be prior or today'})
        return data
