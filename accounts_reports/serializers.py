from rest_framework import serializers
from pesanile_accounting.models import AccountEntry, CustomTransactionDetail, AccountReceivable, AccountPayable,Accounts,Receipt, Payment


class DateWiseSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class PayableReportSerializer(serializers.Serializer):
    payable = serializers.CharField()

class ReceivableReportSerializer(serializers.Serializer):
    receivable = serializers.CharField()

class DateWiseAccountEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEntry
        fields = '__all__'

class PayableAccountEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEntry
        fields = '__all__'

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'

class ReceivableAccountEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountEntry
        fields = '__all__'

class CustomTransactionDetailByTransactionIdSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=100)

class CustomTransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomTransactionDetail
        fields = '__all__'

    def get_custom_field_name(self, obj):
        return obj.custom_field_id.name  # Access the name through the relationship


class TrailBalanceReportSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class GeneralLedgerWithDiffSubLedgersSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class ReceivableListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountReceivable
        fields = ('reference_type','reference_number', 'customer_id', 'customer_name', 'actual_amount', 'amount_due', 'amount_received', 'payment_status', 'company', 'created_by')

class AccountPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPayable
        fields = ('reference_type','reference_number', 'vendor_id', 'vendor_name', 'actual_amount', 'amount_due', 'amount_paid', 'payment_status', 'company', 'created_by')


class StatementOfCashFlowSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

class StatementOfReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'

class StatementOfPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

