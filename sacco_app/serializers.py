from rest_framework import serializers

from pesanile_accounting.models import Accounts,AccountEntry
from .models import *

class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# class DefaultAccountSetUpSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DefaultAccountSetUp
#         fields = '__all__'

class DefaultAccountSetUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultAccountSetUp
        fields = ['code', 'category_type', 'category_name',
                  'account_type', 'account_category', 'glline',
                  'created_at', 'updated_at']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['category_type'] = instance.category_type.type_name if instance.category_type else None
        rep['category_name'] = instance.category_name.category_name if instance.category_name else None
        rep['account_type'] = instance.account_type.name if instance.account_type else None
        rep['account_category'] = instance.account_category.name if instance.account_category else None
        rep['glline'] = instance.glline.name if instance.glline else None
        return rep

class GetAccountRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_number', 'account_type', 'account_category', 'gl_line', 'opening_balance', 'total_balance']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['account_type'] = instance.account_type.name if instance.account_type else None
        rep['account_category'] = instance.account_category.name if instance.account_category else None
        rep['gl_line'] = instance.gl_line.name if instance.gl_line else None
        return rep
    


class GetAccountEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEntry
        fields ='__all__'
