from rest_framework import serializers
from .models import Income
import datetime


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'amount', 'date',
                  'description', "source"]

    def create(self, data):
        self.validate(data)
        return Income.objects.create(**data)

    def validate(self, data):
        if(data['date'] > datetime.date.today()):
            raise serializers.ValidationError(
                {'date': 'Invalid date,date must be prior or today'})
        return data
