from cProfile import label

from django import forms

from sub_part.models import Branch, Company
from .models import *
from django.db.models import Q
from django_select2.forms import ModelSelect2Widget

class ServicePaymentForm(forms.Form):
    user = forms.CharField()
    debit_acc_number = forms.CharField()
    transaction_type = forms.CharField()
    credit_acc_number = forms.CharField()
    amount = forms.FloatField()


class ServicePaymentForms(forms.ModelForm):
    class Meta:
        model = ServicePayment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ServicePaymentForms, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AccountForm(forms.ModelForm):
    branch_name = forms.ModelChoiceField(queryset=Branch.objects.none(), required=True)  # Define branch field

    class Meta:
        model = Accounts
        exclude = ('account_holder', 'account_id', 'current_cleared_balance', 'current_uncleared_balance',
                   'total_balance', 'cr_id', 'loan')  # Exclude 'branch_name' from being auto-generated

        widgets = {
            'gl_line': ModelSelect2Widget(
                model=GLLine,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
            'account_type': ModelSelect2Widget(
                model=AccountType,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
            'account_category': ModelSelect2Widget(
                model=AccountCategory,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
        }

    # def __init__(self, *args, **kwargs):
    #     user = kwargs.pop('created_by')  # Get the user from the view
    #     super(AccountForm, self).__init__(*args, **kwargs)

        # # Add Bootstrap classes to form fields
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'

        # # Filter 'branch_name' queryset based on the user's company
        # if user.is_authenticated:
        #     company_name = user.company

        #     # Optionally set default branch if needed (e.g., first branch for the user)
        #     print('user.is_superuser ',user.is_superuser)
        #     if user.is_superuser:
        #         self.fields['branch_name'].queryset = Branch.objects.all()  # Filter based on company
        #         self.initial['branch_name'] = Branch.objects.all().first()
        #     else:
        #         self.fields['branch_name'].queryset = Branch.objects.filter(company_name=company_name)  # Filter based on company
        #         self.initial['branch_name'] = Branch.objects.filter(company_name=company_name).first()


# ==================== Above Done ==================

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ExchangeRateForm(forms.ModelForm):
    class Meta:
        model = ExchangeRate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExchangeRateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AccountTypeCategoryForm(forms.ModelForm):
    class Meta:
        model = AccountTypeCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountTypeCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountType
        fields = '__all__'
        widgets = {
            'account_type_category': ModelSelect2Widget(
                model=AccountTypeCategory,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AccountTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            print('visible ',visible)
            visible.field.widget.attrs['class'] = 'form-control'


class AccountCategoryForm(forms.ModelForm):
    class Meta:
        model = AccountCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AccountHolderForm(forms.ModelForm):
    class Meta:
        model = AccountHolder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountHolderForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'



class AssetTypeCategoryForm(forms.ModelForm):
    class Meta:
        model = AssetTypeCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AssetTypeCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = '__all__'
        widgets = {
            'asset_type_category': ModelSelect2Widget(
                model=AssetTypeCategory,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AssetTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class GLLineForm(forms.ModelForm):
    class Meta:
        model = GLLine
        fields = '__all__'

        widgets = {
            'asset_type': ModelSelect2Widget(
                model=AssetType,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
            'master_gl': ModelSelect2Widget(
                model='self',
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GLLineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class OverdraftLimitForm(forms.ModelForm):
    class Meta:
        model = OverdraftLimit
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OverdraftLimitForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AccountRestrictionForm(forms.ModelForm):
    class Meta:
        model = AccountRestriction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountRestrictionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TransactionCodeForm(forms.ModelForm):
    class Meta:
        model = TransactionCode
        fields = '__all__'

        widgets = {
            'debit_gl_line': ModelSelect2Widget(
                model=GLLine,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
            'credit_gl_line': ModelSelect2Widget(
                model=GLLine,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
        }

    def __init__(self, *args, **kwargs):
        super(TransactionCodeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ChargeCodeClassificationForm(forms.ModelForm):
    class Meta:
        model = ChargeCodeClassification
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ChargeCodeClassificationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ChargeCodeForm(forms.ModelForm):
    class Meta:
        model = ChargeCode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ChargeCodeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class InterestCodeForm(forms.ModelForm):
    class Meta:
        model = InterestCode
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(InterestCodeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        exclude = ('debit_currency', 'debit_account', 'credit_currency', 'credit_account')

        widgets = {
            'debit_transaction_code': ModelSelect2Widget(
                model=TransactionCode,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
            'credit_transaction_code': ModelSelect2Widget(
                model=TransactionCode,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
            # 'charge_code': ModelSelect2Widget(
            #     model=ChargeCode,
            #     search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            # ),
            'category_of_account': ModelSelect2Widget(
                model=AccountCategory,
                search_fields=['name__icontains'],  # Replace 'name' with the searchable field in RelatedModel
            ),
        }


    def __init__(self, *args, **kwargs):
        super(TransactionTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TransactionDetailForm(forms.ModelForm):
    class Meta:
        model = TransactionDetail
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TransactionDetailForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AccountEntryForm(forms.ModelForm):
    class Meta:
        model = AccountEntry
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountEntryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TellerProfileForm(forms.ModelForm):
    class Meta:
        model = TellerProfile
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TellerProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ('transaction_id', 'exchange_rate_calc_mode', 'exchange_rate_used', 'status', 'created_by')

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('created_by')  # Get the user from the view
        super(TransactionForm, self).__init__(*args, **kwargs)

        # Update the transaction_type field to trigger checkTransactionType
        self.fields['transaction_type'].widget.attrs.update({
            'id': 'id_transaction_type',
            'onchange': 'checkTransactionType()',
            'class': 'form-control'
        })

        # Update specific fields with custom attributes
        self.fields['from_account_id'].widget.attrs.update({
            'id': 'id_from_account_id',
            'onchange': 'updateCurrency("id_from_account_id", "id_from_currency_id")',
            'class': 'form-control'
        })
        self.fields['to_account_id'].widget.attrs.update({
            'id': 'id_to_account_id',
            'onchange': 'updateCurrency("id_to_account_id", "id_to_currency_id")',
            'class': 'form-control'
        })
        self.fields['from_currency_id'].widget.attrs.update({
            'id': 'id_from_currency_id',
            'class': 'form-control',
            'readonly': 'readonly'
        })
        self.fields['to_currency_id'].widget.attrs.update({
            'id': 'id_to_currency_id',
            'class': 'form-control',
            'readonly': 'readonly'
        })

        # Add 'form-control' class to the remaining fields
        for field_name in self.fields:
            if 'class' not in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] = 'form-control'
                # Add Bootstrap classes to form fields
                for visible in self.visible_fields():
                    visible.field.widget.attrs['class'] = 'form-control'

        # Filter 'branch_name' queryset based on the user's company
        if user.is_authenticated:
            company_name = user.company

            # Optionally set default branch if needed (e.g., first branch for the user)
            print('user.is_superuser ', user.is_superuser)
            if user.is_superuser:
                self.fields[
                    'transaction_type'].queryset = TransactionType.objects.all()  # Filter based on company
                self.initial['transaction_type'] = TransactionType.objects.all().first()
            else:
                self.fields['transaction_type'].queryset = TransactionType.objects.filter(
                    company_name=company_name)  # Filter based on company
                self.initial['transaction_type'] = TransactionType.objects.filter(
                    company_name=company_name).first()


    # form field validation
    def clean(self):
        cleaned_data = super(TransactionForm, self).clean()
        from_amount = cleaned_data.get('from_amount')
        to_amount = cleaned_data.get('to_amount')

        # Validation logic
        if not from_amount and not to_amount:
            raise forms.ValidationError(
                "Please provide at least one value: either 'From Amount' or 'To Amount'."
            )
        if from_amount and to_amount:
            raise forms.ValidationError(
                "Please provide only one value: either 'From Amount' or 'To Amount', not both."
            )

        return cleaned_data


class SpecialTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        exclude = ('transaction_id', 'exchange_rate_calc_mode', 'exchange_rate_used', 'status', 'created_by')

    def __init__(self, *args, **kwargs):
        super(SpecialTransactionForm, self).__init__(*args, **kwargs)
        field_order = [
            'transaction_type',
            'from_currency_id', 'from_account_id', 'from_amount',
            'to_currency_id', 'to_account_id', 'to_amount', 'transaction_type_mode'
        ]

        # Update the transaction_type field to trigger checkTransactionType
        self.fields['transaction_type'].widget.attrs.update({
            'id': 'id_transaction_type',
            'onchange': 'checkTransactionType()',
            'class': 'form-control'
        })

        # Update specific fields with custom attributes
        self.fields['from_currency_id'].widget.attrs.update({
            'id': 'id_from_currency_id',
            'onchange': 'updateAccountsByCurrency("id_from_currency_id", document.getElementById('
                        '"id_transaction_type").value, "id_from_account_id", "from")',
            'class': 'form-control',
        })

        self.fields['to_currency_id'].widget.attrs.update({
            'id': 'id_to_currency_id',
            'onchange': 'updateAccountsByCurrency("id_to_currency_id", document.getElementById('
                        '"id_transaction_type").value, "id_to_account_id", "to")',
            'class': 'form-control',
        })

        self.fields['from_account_id'].widget.attrs.update({
            'id': 'id_from_account_id',
            'class': 'form-control',
            'readonly': 'readonly',
        })
        self.fields['to_account_id'].widget.attrs.update({
            'id': 'id_to_account_id',
            'class': 'form-control',
            'readonly': 'readonly',
        })

        # Reorder the fields
        self.fields = {field: self.fields[field] for field in field_order}

        # Add 'form-control' class to the remaining fields
        for field_name in self.fields:
            if 'class' not in self.fields[field_name].widget.attrs:
                self.fields[field_name].widget.attrs['class'] = 'form-control'

    # form field validation
    def clean(self):
        cleaned_data = super(SpecialTransactionForm, self).clean()
        from_amount = cleaned_data.get('from_amount')
        to_amount = cleaned_data.get('to_amount')

        # Validation logic
        if not from_amount and not to_amount:
            raise forms.ValidationError(
                "Please provide at least one value: either 'From Amount' or 'To Amount'."
            )
        if from_amount and to_amount:
            raise forms.ValidationError(
                "Please provide only one value: either 'From Amount' or 'To Amount', not both."
            )

        return cleaned_data


class AccountReceivableForm(forms.ModelForm):
    class Meta:
        model = AccountReceivable
        exclude = ('payment_term_period', 'payment_term_milestone', 'payment_term_amount')

    def __init__(self, *args, **kwargs):
        super(AccountReceivableForm, self).__init__(*args, **kwargs)
        date_fields = ['effective_from', 'due_date', 'amount_due']  # List of your date fields
        for field_name in date_fields:
            if field_name == 'amount_due':
                self.fields[field_name].widget = forms.TextInput(
                    attrs={'type': 'number', 'class': 'form-control', 'readonly': 'readonly'})
            else:
                self.fields[field_name].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AccountPayableForm(forms.ModelForm):
    class Meta:
        model = AccountPayable
        exclude = ('payment_term_period', 'payment_term_milestone', 'payment_term_amount')

    def __init__(self, *args, **kwargs):
        super(AccountPayableForm, self).__init__(*args, **kwargs)
        date_fields = ['effective_from', 'due_date', 'amount_due']  # List of your date fields
        for field_name in date_fields:
            if field_name in self.fields:
                if field_name == 'amount_due':
                    self.fields[field_name].widget = forms.TextInput(
                        attrs={'type': 'number', 'class': 'form-control', 'readonly': 'readonly'})
                else:
                    self.fields[field_name].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReceiptForm(forms.ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReceiptForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TransactionTypeClassificationForm(forms.ModelForm):
    class Meta:
        model = TransactionTypeClassification
        exclude = ('TTC_ID',)

    def __init__(self, *args, **kwargs):
        super(TransactionTypeClassificationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class TransactionTypeModeForm(forms.ModelForm):
    class Meta:
        model = TransactionTypeMode
        exclude = ('mode_id',)

    def __init__(self, *args, **kwargs):
        super(TransactionTypeModeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ReferenceTypeForm(forms.ModelForm):
    class Meta:
        model = ReferenceType
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReferenceTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PaymentComplexityForm(forms.ModelForm):
    class Meta:
        model = PaymentComplexity
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PaymentComplexityForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PaymentAndReceiptForm(forms.Form):
    transaction_type = forms.ChoiceField(choices=[],
                                         widget=forms.Select(
                                             attrs={'class': 'form-control', 'id': 'id_transaction_type',
                                                    'onchange': 'checkTransactionType()'}),
                                         )
    reference_type = forms.ChoiceField(choices=[],
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       )
    receivable = forms.ChoiceField(choices=[],
                                   widget=forms.Select(attrs={'class': 'form-control'}),
                                   )
    payable = forms.ChoiceField(choices=[],
                                widget=forms.Select(attrs={'class': 'form-control', 'required': 'False'}),
                                )
    amount = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    transaction_type_mode = forms.ChoiceField(choices=[],
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control', 'id': 'id_transaction_type_mode',
                                                         'onchange': 'checkTransactionTypeMode()'}),
                                              )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].choices = [('', 'Select an Transaction Type')] + [(data.pk, data.name) for data in
                                                          TransactionType.objects.all()]
        self.fields['reference_type'].choices = [('', 'Select an Reference Type')] + [(data.pk, data.type_name) for data in
                                                        ReferenceType.objects.all()]
        self.fields['receivable'].choices = [('None', 'Select an Account Receivable')] + [(data.reference_number, data.reference_number) for data
                                                                in
                                                                AccountReceivable.objects.filter(
                                                                    ~Q(payment_status='paid'))]
        self.fields['payable'].choices = [('None', 'Select an Account Payable')] + [(data.reference_number, data.reference_number) for data
                                                                in
                                                                AccountPayable.objects.filter(
                                                                    ~Q(payment_status='paid'))]
        self.fields['transaction_type_mode'].choices = [('', 'Select an Transaction Type Mode')] + [(data.pk, data.name) for data in
                                                               TransactionTypeMode.objects.all()]


class UserFinancialAccountMappingForm(forms.ModelForm):
    class Meta:
        model = UserFinancialAccountMapping
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserFinancialAccountMappingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class UserFinancialAccountCategoryForm(forms.ModelForm):
    class Meta:
        model = UserFinancialAccountCategory
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserFinancialAccountCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PostPaymentAndReceiptForm(forms.Form):
    transaction_type = forms.CharField(max_length=50,label='', widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly', 'hidden':'hidden'}))
    # transaction_type_name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    reference_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'readonly'}))
    amount = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    transaction_type_mode = forms.ChoiceField(choices=[],
                                              widget=forms.Select(
                                                  attrs={'class': 'form-control', 'id': 'id_transaction_type_mode',
                                                         'onchange': 'checkTransactionTypeMode()'}),
                                              )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_type_mode'].choices = [('', 'Select an Transaction Type Mode')] + [(data.pk, data.name) for data in
                                                               TransactionTypeMode.objects.all()]

class AccountReceiptForm(forms.ModelForm):
    class Meta:
        model = AccountReceipt
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountReceiptForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class AccountPaymentForm(forms.ModelForm):
    class Meta:
        model = AccountPayment
        exclude = '__all__'

    def __init__(self, *args, **kwargs):
        super(AccountPaymentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CustomFieldTypeForm(forms.ModelForm):
    class Meta:
        model = CustomFieldType
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        super(CustomFieldTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        super(CustomFieldForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class CustomTransactionFieldMappingForm(forms.ModelForm):
    class Meta:
        model = CustomTransactionFieldMapping
        exclude = ('created_by',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('created_by')  # Get the user from the view
        super(CustomTransactionFieldMappingForm, self).__init__(*args, **kwargs)

        # Add Bootstrap classes to form fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        # Filter 'branch_name' queryset based on the user's company
        if user.is_authenticated:
            company_name = user.company_name

            # Optionally set default branch if needed (e.g., first branch for the user)
            print('user.is_superuser ',user.is_superuser)
            if user.is_superuser:
                self.fields['transaction_type'].queryset = TransactionType.objects.all()  # Filter based on company
                self.initial['transaction_type'] = TransactionType.objects.all().first()
            else:
                self.fields['transaction_type'].queryset = TransactionType.objects.filter(company_name=company_name)  # Filter based on company
                self.initial['transaction_type'] = TransactionType.objects.filter(company_name=company_name).first()




class BankRegistrationForm(forms.ModelForm):
    class Meta:
        model = BankRegistration
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BankRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class BusinessGroupForm(forms.ModelForm):
    class Meta:
        model = BusinessGroup
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(BusinessGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
