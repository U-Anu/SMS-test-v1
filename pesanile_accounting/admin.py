from django.contrib import admin
from .models import *
from django.utils.html import format_html  # custom form
from import_export import resources
from import_export.admin import ImportExportModelAdmin


# Register AccountType with list_display and list_filter
class AccountTypeCategoryResource(resources.ModelResource):
    class Meta:
        model = AccountTypeCategory
        import_id_fields = ['account_type_category_id']  # Specify your custom primary key

@admin.register(AccountTypeCategory)
class AccountTypeCategoryAdmin(ImportExportModelAdmin):
    resource_class = AccountTypeCategoryResource
    list_display = ('account_type_category_id', 'name', 'description')
    list_filter = ('name',)


class AccountTypeResource(resources.ModelResource):
    class Meta:
        model = AccountType
        import_id_fields = ['account_type_id']  # Specify your custom primary key

@admin.register(AccountType)
class AccountTypeAdmin(ImportExportModelAdmin):
    resource_class = AccountTypeResource
    list_display = ('account_type_id', 'name', 'account_type_category', 'description')
    list_filter = ('name',)

class AccountCategoryResource(resources.ModelResource):
    class Meta:
        model = AccountCategory
        import_id_fields = ['account_category_id']

@admin.register(AccountCategory)
class AccountCategoryAdmin(ImportExportModelAdmin):
    resource_class = AccountCategoryResource
    list_display = ('account_category_id', 'name', 'description')
    list_filter = ('name',)


class AccountsResource(resources.ModelResource):
    class Meta:
        model = Accounts
        import_id_fields = ['account_number']

@admin.register(Accounts)
class AccountsAdmin(ImportExportModelAdmin):
    resource_class = AccountsResource
    list_display = (
        'account_number', 'short_description', 'base_currency', 'account_holder', 'gl_line',  'account_type', 'account_category',
        'total_balance', 'created_at')
    list_filter = ('account_holder', 'account_type', 'account_category')


class AccountHolderResource(resources.ModelResource):
    class Meta:
        model = AccountHolder
        import_id_fields = ['account_holder_id']

@admin.register(AccountHolder)
class AccountHolderAdmin(ImportExportModelAdmin):
    resource_class = AccountHolderResource
    list_display = ('account_holder_id', 'name', 'type', 'contact_info', 'address')
    list_filter = ('type',)


# class GLLineResource(resources.ModelResource):
#     class Meta:
#         model = GLLine
#         import_id_fields = ['gl_line_id']

# Register AccountType with list_display and list_filter
class GLLineModelResource(resources.ModelResource):
    class Meta:
        model = GLLine
        import_id_fields = ['gl_line_id']  # Specify your custom primary key

@admin.register(GLLine)
class GLLineModelAdmin(ImportExportModelAdmin):
    resource_class = GLLineModelResource
    list_display = ('gl_line_id', 'gl_line_number', 'name', 'description', 'master_gl', 'asset_type')
    list_filter = ('name',)

class AssetTypeCategoryResource(resources.ModelResource):
    class Meta:
        model = AssetTypeCategory
        import_id_fields = ['asset_type_category_id']

@admin.register(AssetTypeCategory)
class AssetTypeCategoryAdmin(ImportExportModelAdmin):
    resource_class = AssetTypeCategoryResource
    list_display = ('asset_type_category_id', 'name', 'description')
    list_filter = ('name',)



class AssetTypeResource(resources.ModelResource):
    class Meta:
        model = AssetType
        import_id_fields = ['asset_type_id']

@admin.register(AssetType)
class AssetTypeAdmin(ImportExportModelAdmin):
    resource_class = AssetTypeResource
    list_display = ('asset_type_id', 'name', 'asset_type_category', 'description')
    list_filter = ('name',)


class TransactionCodeResource(resources.ModelResource):
    class Meta:
        model = TransactionCode
        import_id_fields = ['transaction_code_id']

@admin.register(TransactionCode)
class TransactionCodeAdmin(ImportExportModelAdmin):
    resource_class = TransactionCodeResource
    list_display = (
        'transaction_code_id', 'name', 'debit_gl_line', 'credit_gl_line', 'template_description', 'overdraft_check')
    list_filter = ('name', 'overdraft_check')


class ChargeCodeResource(resources.ModelResource):
    class Meta:
        model = ChargeCode
        import_id_fields = ['charge_code_id']

@admin.register(ChargeCode)
class ChargeCodeAdmin(ImportExportModelAdmin):
    resource_class = ChargeCodeResource
    list_display = (
        'charge_code_id', 'name', 'charge_amount', 'currency', 'gl_line_to_credit', 'transaction_code_to_use')
    list_filter = ('name', 'currency')


class TransactionTypeResource(resources.ModelResource):
    class Meta:
        model = TransactionType
        import_id_fields = ['transaction_type_id']

@admin.register(TransactionType)
class TransactionTypeAdmin(ImportExportModelAdmin):
    resource_class = TransactionTypeResource
    list_display = (
        'transaction_type_id', 'name', 'debit_transaction_code', 'credit_transaction_code',
        'description')
    list_filter = ('name',)


class TransactionResource(resources.ModelResource):
    class Meta:
        model = Transaction
        import_id_fields = ['transaction_id']

@admin.register(Transaction)
class TransactionAdmin(ImportExportModelAdmin):
    resource_class = TransactionResource
    list_display = (
        'transaction_id', 'transaction_type', 'from_account_id', 'from_currency_id', 'from_amount', 'to_account_id',
        'to_currency_id', 'to_amount', 'exchange_rate_calc_mode', 'exchange_rate_used',
        'transaction_date_time', 'status')
    list_filter = ('transaction_type', 'from_account_id', 'to_account_id', 'status')


# Continue the rest in this format
class TransactionDetailResource(resources.ModelResource):
    class Meta:
        model = TransactionDetail
        import_id_fields = ['transaction_detail_id']

@admin.register(TransactionDetail)
class TransactionDetailAdmin(ImportExportModelAdmin):
    resource_class = TransactionDetailResource
    list_display = ('transaction_detail_id', 'transaction', 'detail_key', 'detail_value')
    list_filter = ('transaction',)


class ReconciliationResource(resources.ModelResource):
    class Meta:
        model = Reconciliation
        import_id_fields = ['reconciliation_id']

@admin.register(Reconciliation)
class ReconciliationAdmin(ImportExportModelAdmin):
    resource_class = ReconciliationResource
    list_display = ('reconciliation_id', 'account', 'date', 'status')
    list_filter = ('account', 'status')


class AccountEntryResource(resources.ModelResource):
    class Meta:
        model = AccountEntry
        import_id_fields = ['entry_ID']

@admin.register(AccountEntry)
class AccountEntryAdmin(ImportExportModelAdmin):
    resource_class = AccountEntryResource
    list_display = (
        'entry_ID', 'transaction_id', 'transaction_code', 'account_number', 'amount', 'currency', 'debit_credit_marker',
        'entry_date')
    list_filter = ('entry_date', 'transaction_id', 'account_number')


class CurrencyResource(resources.ModelResource):
    class Meta:
        model = Currency
        import_id_fields = ['currency_id']

@admin.register(Currency)
class CurrencyAdmin(ImportExportModelAdmin):
    resource_class = CurrencyResource
    list_display = (
        'currency_id', 'currency_code', 'currency_name', 'symbol', 'created_at', 'updated_at')
    list_filter = ('currency_id', 'currency_code', 'currency_name')


class ExchangeRateResource(resources.ModelResource):
    class Meta:
        model = ExchangeRate
        import_id_fields = ['exchange_rate_id']

@admin.register(ExchangeRate)
class ExchangeRateAdmin(ImportExportModelAdmin):
    resource_class = ExchangeRateResource
    list_display = (
        'exchange_rate_id', 'from_currency', 'to_currency', 'buy_rate', 'sell_rate',
        'mid_rate', 'valid_from', 'valid_to', 'created_at', 'updated_at')
    list_filter = ('exchange_rate_id', 'from_currency', 'to_currency')

class ReferenceTypeResource(resources.ModelResource):
    class Meta:
        model = ReferenceType
        import_id_fields = ['type_name']

@admin.register(ReferenceType)
class ReferenceTypeAdmin(ImportExportModelAdmin):
    resource_class = ReferenceTypeResource
    list_display = (
        'type_id', 'type_name', 'description')
    # list_filter = ('type_name')

# class CompanyResource(resources.ModelResource):
#     class Meta:
#         model = Company
#         import_id_fields = ['company_id']

# @admin.register(Company)
# class CompanyAdmin(ImportExportModelAdmin):
#     resource_class = CompanyResource
#     list_display = (
#         'company_id', 'company_name', 'local_currency', 'address', 'phone',
#         'email', 'incorporation_number', 'website', 'number_of_branches',
#         'number_of_staffs', 'end_of_financial_year', 'end_of_month_date', 'amount_rounded_to', 'created_at',
#         'updated_at')
#     list_filter = ('company_id', 'company_name', 'local_currency')


class TellerProfileResource(resources.ModelResource):
    class Meta:
        model = TellerProfile
        import_id_fields = ['user']

@admin.register(TellerProfile)
class TellerProfileAdmin(ImportExportModelAdmin):
    resource_class = TellerProfileResource
    list_display = (
        'user', 'cash_withdrawal_limit', 'cash_deposit_limit', 'currency_exchange_limit',
        'created_at', 'updated_at'
    )


class CommonRegistrationResource(resources.ModelResource):
    class Meta:
        model = CommonRegistration
        import_id_fields = ['id']

@admin.register(CommonRegistration)
class CommonRegistrationAdmin(ImportExportModelAdmin):
    resource_class = CommonRegistrationResource
    list_display = ('id', 'name', 'category_name', 'register_id', 'register_as', 'created_at')
    list_filter = ('id', 'name', 'register_as', 'category_name')


class CustomTransactionDetailResource(resources.ModelResource):
    class Meta:
        model = CustomTransactionDetail
        import_id_fields = ['ctd_id']

@admin.register(CustomTransactionDetail)
class CustomTransactionDetailAdmin(ImportExportModelAdmin):
    resource_class = CustomTransactionDetailResource
    list_display = ('ctd_id', 'transaction_id', 'custom_field_id', 'field_value', 'created_at')
    list_filter = ('transaction_id',)

class AccountPayableResource(resources.ModelResource):
    class Meta:
        model = AccountPayable
        import_id_fields = ['id']  # Assuming `id` is the primary key for this model

@admin.register(AccountPayable)
class AccountPayableAdmin(ImportExportModelAdmin):
    resource_class = AccountPayableResource
    list_display = (
        'reference_type', 'reference_number', 'effective_from', 'vendor_name', 'vendor_id',
        'actual_amount', 'payment_complexity', 'payment_term_period', 'payment_term_milestone',
        'payment_term_amount', 'amount_paid', 'amount_due', 'due_date', 'currency',
        'payment_status', 'internal_notes', 'vendor_communication', 
        # 'created_by', 
        
    )
    list_filter = ('reference_type', 'vendor_name', 'payment_status', 'currency')

class AccountReceivableResource(resources.ModelResource):
    class Meta:
        model = AccountReceivable
        import_id_fields = ['id']  # Assuming `id` is the primary key for this model

@admin.register(AccountReceivable)
class AccountReceivableAdmin(ImportExportModelAdmin):
    resource_class = AccountReceivableResource
    list_display = (
        'reference_type', 'reference_number', 'effective_from', 'student_name', 'student_id', 'bank',
        'actual_amount', 'payment_complexity', 'payment_term_period', 'payment_term_milestone',
        'payment_term_amount', 'amount_received', 'amount_due', 'due_date', 'currency',
        'payment_status', 'internal_notes', 'customer_communication', 
    )
    list_filter = ('reference_type', 'student_name', 'payment_status', 'currency',)

class PaymentResource(resources.ModelResource):
    class Meta:
        model = Payment
        import_id_fields = ['id']  # Assuming `id` is the primary key for this model

@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    resource_class = PaymentResource
    list_display = (
        'account_payable', 'amount_paid', 'payment_date', 'reference_number',
        # 'created_by', 
        'created_at', 'updated_at'
    )
    list_filter = ('account_payable', 'payment_date')

class ReceiptResource(resources.ModelResource):
    class Meta:
        model = Receipt
        import_id_fields = ['id']  # Assuming `id` is the primary key for this model

@admin.register(Receipt)
class ReceiptAdmin(ImportExportModelAdmin):
    resource_class = ReceiptResource
    list_display = (
        'account_receivable', 'amount_received', 'receipt_date', 'reference_number',
        # 'created_by',
        'created_at', 'updated_at'
    )
    list_filter = ('account_receivable', 'receipt_date', ) #'created_by'

class TransactionTypeModeResource(resources.ModelResource):
    class Meta:
        model = TransactionTypeMode
        import_id_fields = ['mode_id']  # Using the custom primary key `mode_id`

@admin.register(TransactionTypeMode)
class TransactionTypeModeAdmin(ImportExportModelAdmin):
    resource_class = TransactionTypeModeResource
    list_display = (
        'mode_id', 'name', 'description', 'created_by', 'created_at', 'updated_at'
    )
    list_filter = ('name', 'created_by', 'created_at')

class TransactionTypeClassificationResource(resources.ModelResource):
    class Meta:
        model = TransactionTypeClassification
        import_id_fields = ['TTC_ID']  # Using the custom primary key `mode_id`

@admin.register(TransactionTypeClassification)
class TransactionTypeClassificationAdmin(ImportExportModelAdmin):
    resource_class = TransactionTypeClassificationResource
    list_display = (
        'TTC_ID', 'name', 'description', 'created_by'
    )
    list_filter = ('name', 'created_by', 'created_at')


class BusinessGroupResource(resources.ModelResource):
    class Meta:
        model = BusinessGroup
        import_id_fields = ['business_group_id']

@admin.register(BusinessGroup)
class BusinessGroupAdmin(ImportExportModelAdmin):
    resource_class = BusinessGroupResource
    list_display = ('business_group_id', 'name', 'description')
    list_filter = ('name',)

class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department
        import_id_fields = ['dept_id']

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    resource_class = DepartmentResource
    list_display = ('dept_id', 'name', 'description')
    list_filter = ('name',)


# class BranchResource(resources.ModelResource):
#     class Meta:
#         model = Branch
#         import_id_fields = ['branch_id']

# @admin.register(Branch)
# class BranchAdmin(ImportExportModelAdmin):
#     resource_class = BranchResource
#     list_display = ('branch_id', 'branch_name', 'company_name', 'description','created_by')
#     list_filter = ('branch_name','company_name','created_by')


# admin.site.register(ReferenceType)
admin.site.register(CustomTransactionFieldMapping)
admin.site.register(BankRegistration)
