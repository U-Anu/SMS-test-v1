from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q
from .scripts import *
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # token['purpose'] = user.purpose # add some extra
        return token

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'


class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCategory
        fields = '__all__'


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'


class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        fields = '__all__'


class GLLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLLine
        fields = '__all__'


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'


class TransactionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCode
        fields = '__all__'


class ChargeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCode
        fields = '__all__'


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = '__all__'


class ReconciliationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reconciliation
        fields = '__all__'


class ServicePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePayment
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('transaction_id', 'exchange_rate_calc_mode', 'exchange_rate_used', 'status', 'created_by')

    def validate(self, data):
        from_amount = data.get('from_amount')
        to_amount = data.get('to_amount')

        # Validation logic
        if not from_amount and not to_amount:
            raise serializers.ValidationError(
                "Please provide at least one value: either 'From Amount' or 'To Amount'."
            )
        if from_amount and to_amount:
            raise serializers.ValidationError(
                "Please provide only one value: either 'From Amount' or 'To Amount', not both."
            )

        return data


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = '__all__'


class AccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountCategory
        fields = '__all__'


class AccountHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHolder
        fields = '__all__'


class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'


class GLLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = GLLine
        fields = '__all__'


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = '__all__'


class OverdraftLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverdraftLimit
        fields = '__all__'


class AccountRestrictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountRestriction
        fields = '__all__'


class TransactionCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionCode
        fields = '__all__'


class ChargeCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargeCode
        fields = '__all__'


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'


class TransactionTypeClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTypeClassification
        fields = '__all__'


class TransactionTypeModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTypeMode
        fields = '__all__'


class TransactionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetail
        fields = '__all__'


class TellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TellerProfile
        fields = '__all__'


class ReferenceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceType
        fields = '__all__'


class PaymentComplexitySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentComplexity
        fields = '__all__'


class AccountPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountPayable
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = '__all__'


class UserFinancialAccountMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFinancialAccountMapping
        fields = '__all__'


class UserFinancialAccountCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFinancialAccountCategory
        fields = '__all__'


class AccountReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountReceivable
        fields = '__all__'

class AccountReceivableAmountSerializer(serializers.Serializer):
    new_amount = serializers.FloatField(required=True)



class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class TransactionSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('transaction_id', 'exchange_rate_calc_mode', 'exchange_rate_used', 'status', 'created_by')

    def validate(self, data):
        from_amount = data.get('from_amount')
        to_amount = data.get('to_amount')

        # Validation logic
        if not from_amount and not to_amount:
            raise serializers.ValidationError(
                "Please provide at least one value: either 'From Amount' or 'To Amount'."
            )
        if from_amount and to_amount:
            raise serializers.ValidationError(
                "Please provide only one value: either 'From Amount' or 'To Amount', not both."
            )

        return data


class SpecialTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude = ('transaction_id', 'exchange_rate_calc_mode', 'exchange_rate_used', 'status', 'created_by')

    def validate(self, data):
        from_amount = data.get('from_amount')
        to_amount = data.get('to_amount')

        # Validation logic
        if not from_amount and not to_amount:
            raise serializers.ValidationError(
                "Please provide at least one value: either 'From Amount' or 'To Amount'."
            )
        if from_amount and to_amount:
            raise serializers.ValidationError(
                "Please provide only one value: either 'From Amount' or 'To Amount', not both."
            )

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'groups', 'user_permissions', 'is_superuser', 'is_active', 'last_login')


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('is_staff', 'groups', 'user_permissions', 'is_superuser', 'password', 'last_login')


class PaymentAndReceiptSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(
        choices=[],  # Initialize with an empty list
        help_text='Select a transaction type'
    )
    receivable = serializers.ChoiceField(
        choices=[('None', 'Select an Account Receivable')],
        required=False,
        help_text='Select an account receivable'
    )
    payable = serializers.ChoiceField(
        choices=[('None', 'Select an Account Payable')],
        required=False,
        help_text='Select an account payable'
    )
    amount = serializers.FloatField(
        help_text='Enter the amount'
    )
    transaction_type_mode = serializers.ChoiceField(
        choices=[],  # Initialize with an empty list
        help_text='Select a transaction type mode'
    )
    input_params_values = serializers.JSONField(initial=dict)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically populate transaction type choices
        self.fields['transaction_type'].choices = [
            (data.pk, data.name) for data in TransactionType.objects.all()
        ]

        # Dynamically populate receivable choices
        receivable_choices = [
            (data.reference_number, data.reference_number) for data in
            AccountReceivable.objects.filter(~Q(payment_status='paid'))
        ]
        self.fields['receivable'].choices = [('None', 'Select an Account Receivable')] + receivable_choices

        # Dynamically populate payable choices
        payable_choices = [
            (data.reference_number, data.reference_number) for data in
            AccountPayable.objects.filter(~Q(payment_status='paid'))
        ]
        self.fields['payable'].choices = [('None', 'Select an Account Payable')] + payable_choices

        # Dynamically populate transaction type mode choices
        self.fields['transaction_type_mode'].choices = [
            (data.pk, data.name) for data in TransactionTypeMode.objects.all()
        ]

    def validate(self, data):
        transaction_type = data.get('transaction_type')
        receivable = data.get('receivable')
        payable = data.get('payable')

        if receivable == 'None' and payable == 'None':
            raise serializers.ValidationError('Receivable and payable should not be empty.')

        txn_obj = validate_transaction_type(transaction_type)
        if txn_obj is None:
            raise serializers.ValidationError('Invalid transaction type.')

        if txn_obj.name.lower() == 'payment' and payable == 'None':
            raise serializers.ValidationError('Kindly select the payable.')

        if txn_obj.name.lower() == 'receipt' and receivable == 'None':
            raise serializers.ValidationError('Kindly select the receivable.')

        return data


class BranchSerialize(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class CommonRegistrationSerialize(serializers.ModelSerializer):
    class Meta:
        model = CommonRegistration
        fields = '__all__'

class AllTransactionSerializer(serializers.Serializer):
    transaction_type_id = serializers.CharField()  # ST002
    company_id = serializers.CharField()  # Channel id
    amount = serializers.FloatField()
    input_params_values = serializers.JSONField(initial=dict)

    def validate(self, attrs):
        if not TransactionType.objects.filter(pk=attrs["transaction_type_id"]).exists():
            raise serializers.ValidationError(
                "Transaction Type with provided id does not exist"
            )
        elif not Company.objects.filter(pk=attrs["company_id"]).exists():
            raise serializers.ValidationError("Company with provided id does not exist")
        # add more validation
        return attrs

class FundsTransferSerializer(serializers.Serializer):
    from_account_no = serializers.CharField()
    to_account_no = serializers.CharField()
    transaction_type = serializers.CharField()
    amount = serializers.FloatField()

    def validate_from_account_no(self, value):
        obj = Accounts.objects.filter(account_id = value)
        if not obj.exists():
            raise serializers.ValidationError("Invalid From Account Number")
        return value

    def validate_to_account_no(self, value):
        obj = Accounts.objects.filter(account_id = value)
        if not obj.exists():
            raise serializers.ValidationError("Invalid To Account Number")
        return value

    def validate_transaction_type(self, value):
        print('value ',value)
        txn_obj = TransactionType.objects.filter(pk = value)
        print('txn_obj ',txn_obj)
        if not txn_obj.exists():
            raise serializers.ValidationError("Invalid Transaction Type")
        return value

    def validate(self, data):
        if data['from_account_no'] == data['to_account_no']:
            raise serializers.ValidationError("From and to account numbers must be different.")
        return data

class BankRegistrationSerialize(serializers.ModelSerializer):
    class Meta:
        model = BankRegistration
        fields = '__all__'

class BankToMemberAccountSerializer(serializers.Serializer):
    bank_id = serializers.CharField()
    member_id = serializers.CharField()
    reference_type = serializers.CharField()
    reference_id = serializers.CharField()
    total_amount = serializers.CharField()
    member_acc_id = serializers.CharField()
    member_amount = serializers.CharField()
    transaction_type = serializers.CharField()

    def validate_bank_id(self, value):
        obj = BankRegistration.objects.filter(code = value)
        if not obj.exists():
            raise serializers.ValidationError("Invalid Bank Id")
        return value

    def validate_transaction_type(self, value):
        obj = TransactionType.objects.filter(pk = value)
        if not obj.exists():
            raise serializers.ValidationError("Invalid Transaction Type Id")
        return value


class MemberToBankAccountSerializer(serializers.Serializer):
    bank_id = serializers.CharField()
    member_id = serializers.CharField()
    reference_type = serializers.CharField()
    reference_id = serializers.CharField()
    total_amount = serializers.CharField()
    member_acc_id = serializers.CharField()
    member_amount = serializers.CharField()
    transaction_type = serializers.CharField()

    def validate_bank_id(self, value):
        obj = BankRegistration.objects.filter(code = value)
        if not obj.exists():
            raise serializers.ValidationError("Invalid Bank Id")
        return value

    def validate_transaction_type(self, value):
        obj = TransactionType.objects.filter(pk = value)
        if not obj.exists():
            raise serializers.ValidationError("Invalid Transaction Type Id")
        return value

class GetCompanyAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
        fields = ['account_id', 'account_number', 'account_type', 'account_category', 'gl_line', 'opening_balance', 'total_balance', 'company']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['account_type'] = instance.account_type.name if instance.account_type else None
        rep['account_category'] = instance.account_category.name if instance.account_category else None
        rep['gl_line'] = instance.gl_line.name if instance.gl_line else None
        return rep


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','middle_name','last_name','email','phone_number','password']
