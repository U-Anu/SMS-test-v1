from rest_framework import serializers
from .models import *
from pesanile_accounting.models import Accounts

class LoanRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRegistration
        fields = '__all__'


class GetAccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_id','account_number', 'opening_balance', 'total_balance','account_type', 'account_category', 'gl_line', 'loan', ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['account_type'] = instance.account_type.name if instance.account_type else None
        rep['account_category'] = instance.account_category.name if instance.account_category else None
        rep['gl_line'] = instance.gl_line.name if instance.gl_line else None
        return rep
