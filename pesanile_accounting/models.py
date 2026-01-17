from email.policy import default
from enum import unique
from random import choices
# from loan_app.models import *
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager
)
import random
# from sub_part.models import User,Company,Branch
# from loan_app.models import LoanRegistration


def generate_custom_id(prefix=None):
    print('prefix ', prefix)
    if prefix is not None:
        return str(str(prefix) + '-' + str(random.randint(11111, 99999)))
    else: 
        return str('NA' + '-' + str(random.randint(11111, 99999)))


# Create your models here.

# ============= Company Registration ==============================
# class Company(models.Model):
#     company_id = models.CharField(max_length=50, primary_key=True, editable=False)  # null=False,blank=False
#     company_name = models.CharField(max_length=50, null=True, default='NA')
#     local_currency = models.ForeignKey('pesanile_accounting.Currency', on_delete=models.CASCADE,
#                                        related_name='local_currency', null=True)
#     address = models.CharField(max_length=100, null=True)
#     phone = models.CharField(max_length=15, null=True)
#     email = models.EmailField(null=True)
#     incorporation_number = models.CharField(max_length=100,null=True)
#     website = models.URLField(max_length=200, null=True)
#     number_of_branches = models.IntegerField(null=True)
#     number_of_staffs = models.IntegerField(null=True)
#     end_of_financial_year = models.DateField(null=True)
#     end_of_month_date = models.DateField(null=True)  # manually captured by the Company admin
#     amount_rounded_to = models.IntegerField(default=2)

#     created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name="created_by_User", null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def save(self, *args, **kwargs):
#         if not self.company_id:
#             self.company_id = generate_custom_id("COMP")
#             new = True
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return 'NA' if self.company_name is None else self.company_name

#     class Meta:
#         verbose_name_plural = 'Companies'
#         ordering = ['-created_at']

# class Branch(models.Model):
#     branch_id = models.CharField(max_length=50,primary_key=True, editable=False)
#     branch_name = models.CharField(max_length=50)
#     company_name = models.ForeignKey(Company, editable=False, on_delete=models.CASCADE, related_name='company_name_for_branch')
#     description = models.TextField()
#     created_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name="created_by_branch", null=True)
#     update_by = models.ForeignKey(User, editable=False, on_delete=models.CASCADE, related_name="update_by_branch", null=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return str(self.branch_name)

#     def save(self, *args, **kwargs):
#         if not self.branch_id:
#             self.branch_id = generate_custom_id("BR")
#             new = True
#         super().save(*args, **kwargs)

#     class Meta:
#         ordering = ['-created_at']

class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        return self.create_user(email, password, **other_fields)

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide a valid email address"))

        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user


# class User(AbstractBaseUser, PermissionsMixin):
#     first_name = models.CharField(max_length=100, blank=False, null=True)
#     middle_name = models.CharField(max_length=100, blank=True, null=True)
#     last_name = models.CharField(max_length=100, blank=False, null=True)
#     email = models.EmailField(_("email address"), unique=True)
#     phone_number = models.CharField(max_length=15, null=True, blank=False)
#     company_name = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name='company_names', null=True,
#                                      blank=False)
#     branch_name = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_company_name_user', null=True, blank=True)
#     is_customer = models.BooleanField(default=False)
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)

#     objects = CustomUserManager()

#     REQUIRED_FIELDS = ["first_name", "middle_name", "last_name", "phone_number"]

#     USERNAME_FIELD = "email"

#     def __str__(self) -> str:
#         return str(self.first_name)
#_________________________________________---------------------__________________________--------------------



class CommonForMT(models.Model):
    # company_name = models.ForeignKey(Company, null=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_company')
    # branch_name = models.ForeignKey(Branch, null=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_branch',)

    # created_by = models.ForeignKey('sub_part.User', on_delete=models.CASCADE,    related_name='%(class)s_created_by', null=True,blank=True,
    #                                editable=False)
    # updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_updated_at', null=True,
    #                                editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
class CommonForPreSetUp(models.Model):
    created_by = models.ForeignKey('sub_part.User', on_delete=models.CASCADE, related_name='%(class)s_created_at_default', null=True,blank=True,
                                   editable=False)
    # updated_by = models.ForeignKey('sub_part.User', on_delete=models.CASCADE, related_name='%(class)s_updated_at_default', null=True,
    #                                editable=False)
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        abstract = True
# ======= start currency and multi currency concept there ===============
class Currency(CommonForPreSetUp):
    currency_id = models.CharField(max_length=10, primary_key=True, editable=False)
    currency_code = models.CharField(max_length=10, unique=True)
    currency_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)

    def save(self, *args, **kwargs):
        if not self.currency_id:
            self.currency_id = generate_custom_id(self.currency_code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.currency_code}"

    class Meta:
        verbose_name_plural = "Currencies"
        ordering = ['-created_at']


class ExchangeRate(CommonForPreSetUp):
    exchange_rate_id = models.CharField(max_length=10, primary_key=True, editable=False)
    from_currency = models.ForeignKey(Currency, related_name='from_currency', null=True, on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Currency, related_name='to_currency', null=True, on_delete=models.CASCADE)
    buy_rate = models.FloatField()
    sell_rate = models.FloatField()
    mid_rate = models.FloatField()
    valid_from = models.DateField()
    valid_to = models.DateField()



    def save(self, *args, **kwargs):
        if not self.exchange_rate_id:
            self.exchange_rate_id = generate_custom_id(str(self.from_currency) + '-' + str(self.to_currency))
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.exchange_rate_id}"


# ======= end currency and multi currency concept there ===============


# AccountType Model
class AccountTypeCategory(CommonForPreSetUp):
    account_type_category_id = models.CharField(max_length=10, primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        if not self.account_type_category_id:
            self.account_type_category_id = generate_custom_id('ATC')
        super().save(*args, **kwargs)

    class Meta:
        # ordering = ["horn_length"]
        verbose_name_plural = "Account Type Category"
        ordering = ['-created_at']

# AccountType Model
class AccountType(CommonForPreSetUp):
    account_type_id = models.CharField(max_length=10, primary_key=True)
    account_type_category = models.ForeignKey(AccountTypeCategory, on_delete=models.CASCADE, blank=True,null=True,related_name='account_category_name')
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)
    def save(self, *args, **kwargs):
        if not self.account_type_id:
            self.account_type_id = generate_custom_id('AT')
        super().save(*args, **kwargs)

    class Meta:
        # ordering = ["horn_length"]
        verbose_name_plural = "Account Type"
        ordering = ['-created_at']

# AccountCategory Model
class AccountCategory(CommonForPreSetUp):
    account_category_id = models.CharField(max_length=50, editable=False,primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        if not self.account_category_id:
            self.account_category_id = generate_custom_id('AT')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Account Categories"
        ordering = ['-created_at']


# AccountHolder Model
class AccountHolder(CommonForMT):
    account_holder_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    address = models.CharField(max_length=255)



    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Account Holder"
        ordering = ['-created_at']


class AssetTypeCategory(CommonForPreSetUp):
    asset_type_category_id = models.CharField(max_length=10,primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.asset_type_category_id:
            self.asset_type_category_id = generate_custom_id('ATC')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Asset Type Category"
        ordering = ['-created_at']

class AssetType(CommonForPreSetUp):
    asset_type_id = models.CharField(max_length=10,primary_key=True, editable=False)
    asset_type_category = models.ForeignKey(AssetTypeCategory, on_delete=models.CASCADE,blank=True,null=True, related_name='asset_type_category')
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)


    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.asset_type_id:
            print('self.asset_type_id ',self.asset_type_id)
            self.asset_type_id = generate_custom_id('AT')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Asset Type"
        ordering = ['-created_at']


class GLLine(CommonForPreSetUp):
    gl_line_id = models.CharField(max_length=50,primary_key=True, editable=False)
    gl_line_number = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=False)
    description = models.CharField(max_length=255)
    master_gl = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL,
                                  related_name="master_glline")
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE, related_name="asset_type")


    def __str__(self):
        return str(self.asset_type.name)+'-'+str(self.name)

    def save(self, *args, **kwargs):
        if not self.gl_line_id:
            print('self.gl_line_id ',self.gl_line_id)
            self.gl_line_id = generate_custom_id('GLID')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "GL Line"
        ordering = ['-created_at']


# Accounts Model
class Accounts(CommonForMT):
    account_id = models.CharField(max_length=50,primary_key=True)
    account_number = models.CharField(max_length=255, unique=True, editable=True)
    short_description = models.CharField(max_length=250, null=True, blank=True)
    account_holder = models.ForeignKey(AccountHolder, on_delete=models.CASCADE, related_name="account_holder",
                                       null=True, blank=True)
    student_id = models.ForeignKey('sub_part.StudentMain', on_delete=models.CASCADE, related_name="student",
                                       null=True, blank=True)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company", null=True, blank=True)
    # branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="branch", null=True, blank=True)
    gl_line = models.ForeignKey(GLLine, on_delete=models.CASCADE, related_name="glline", null=True, blank=True)
    account_type = models.ForeignKey(AccountType, on_delete=models.CASCADE, related_name="account_type")
    account_category = models.ForeignKey(AccountCategory, on_delete=models.CASCADE, related_name="account_category")
    base_currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    cr_id = models.ForeignKey('CommonRegistration', on_delete=models.CASCADE, related_name='common_registration_id', null=True, blank=True)
    # loan = models.ForeignKey(LoanRegistration, on_delete=models.CASCADE, related_name='loan_reg_id', null=True, blank=True)
    overdraft_limit = models.FloatField(default=0)
    opening_balance = models.FloatField(default=0)
    current_cleared_balance = models.FloatField(default=0)
    current_uncleared_balance = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)
    bank = models.ForeignKey('pesanile_accounting.BankRegistration', on_delete=models.CASCADE, related_name='bank_registration_code', null=True, blank=True)


    def __str__(self):
        return self.short_description or ""


    def save(self, *args, **kwargs):
        if not self.account_id:
            print('self.account_id ',self.account_id)
            self.account_id = generate_custom_id('AC')
            print('self.account_id ',self.account_id)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Account"
        # ordering = ['-created_at']


class OverdraftLimit(CommonForMT):
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="account")
    limit_amount = models.FloatField()


    def __str__(self):
        return f"Overdraft Limit for Account {self.account_id}"

    class Meta:
        verbose_name_plural = "Overdraft Limit"
        ordering = ['-created_at']


class AccountRestriction(CommonForMT):
    class RestrictionType(models.TextChoices):
        DEBIT = 'debit', 'Debit'
        CREDIT = 'credit', 'Credit'

    account = models.ForeignKey('Accounts', on_delete=models.CASCADE)
    restriction_type = models.CharField(max_length=6, choices=RestrictionType.choices)
    restriction_amount = models.FloatField()



    def __str__(self):
        return f"Restriction {self.restriction_type} for Account {self.account_id}"

    class Meta:
        verbose_name_plural = "Account Restriction"
        ordering = ['-created_at']


# TransactionCode Model
class TransactionCode(CommonForMT):
    transaction_code_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    debit_gl_line = models.ForeignKey('GLLine', related_name='debit_transaction_codes', on_delete=models.CASCADE)
    credit_gl_line = models.ForeignKey('GLLine', related_name='credit_transaction_codes', on_delete=models.CASCADE)
    template_description = models.CharField(max_length=255)
    overdraft_check = models.BooleanField(default=False)



    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Transaction Code"
        ordering = ['-created_at']


class ChargeCodeClassification(CommonForPreSetUp):
    charge_code_cls_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

# ChargeCode Model
class ChargeCode(CommonForMT):
    charge_code_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    charge_code_classification = models.ForeignKey(ChargeCodeClassification, on_delete=models.CASCADE, related_name='ccc', null=True, blank=False)
    CHARGE_MODE = (('flat', 'FLAT'), ('percentage', 'PERCENTAGE'))
    charge_mode = models.CharField(max_length=10, choices=CHARGE_MODE, null=True)
    charge_amount = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_for_charge', null=True)
    gl_line_to_credit = models.ForeignKey(GLLine, on_delete=models.CASCADE, related_name="gl_line_to_credit")
    transaction_code_to_use = models.ForeignKey(TransactionCode, on_delete=models.CASCADE,
                                                related_name="transaction_code_to_use")



    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Charge Code"
        ordering = ['-created_at']


# InterestCode Model
class InterestCode(CommonForMT):
    interest_code_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    INTEREST_MODE = (('flat', 'FLAT'), ('percentage', 'PERCENTAGE'))
    interest_mode = models.CharField(max_length=10, choices=INTEREST_MODE, null=True)
    interest_amount = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='currency_for_interest', null=True)
    gl_line_to_credit = models.ForeignKey(GLLine, on_delete=models.CASCADE, related_name="gl_line_to_credit_interest")
    transaction_code_to_use = models.ForeignKey(TransactionCode, on_delete=models.CASCADE,
                                                related_name="transaction_code_to_use_interest")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Interest Code"
        ordering = ['-created_at']


# TransactionType Model
class TransactionType(models.Model):
    transaction_type_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    debit_transaction_code = models.ForeignKey(TransactionCode, related_name="debit_transaction_types",
                                               on_delete=models.CASCADE, null=True, blank=True)
    credit_transaction_code = models.ForeignKey(TransactionCode, related_name="credit_transaction_types",
                                                on_delete=models.CASCADE, null=True, blank=True)
    # charge_code = models.ForeignKey(ChargeCode, on_delete=models.CASCADE, null=True, blank=True, related_name="charge_code",)
    charge_code = models.ManyToManyField(ChargeCode, null=True, blank=True, related_name="charge_code",)
    category_of_account = models.ForeignKey(AccountCategory, on_delete=models.CASCADE, null=True, blank=True,
                                            help_text="when transaction type will be payment or "
                                                      "receipt then only defined")
    txn_type_classification = models.ManyToManyField('TransactionTypeClassification', null=True, blank=True)
    # added associated multi value fields
    debit_currency = models.TextField(null=True)
    debit_account = models.TextField(null=True)
    credit_currency = models.TextField(null=True)
    credit_account = models.TextField(null=True)

    description = models.CharField(max_length=255)

    company_name = models.ForeignKey('sub_part.Company', null=True, editable=False, on_delete=models.CASCADE, related_name='%(class)s_company')
    created_by = models.ForeignKey('sub_part.User', on_delete=models.CASCADE, related_name='%(class)s_created_at', null=True,
                                   editable=False)
    updated_by = models.ForeignKey('sub_part.User', on_delete=models.CASCADE, related_name='%(class)s_updated_at', null=True,
                                   editable=False)
    created_at = models.DateTimeField(null=True,auto_now_add=True)
    updated_at = models.DateTimeField(null=True,auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Transaction Type"
        ordering = ['-created_at']


class TransactionTypeClassification(CommonForPreSetUp):
    TTC_ID = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)


    def save(self, *args, **kwargs):
        if not self.TTC_ID:
            self.TTC_ID = generate_custom_id('TTC')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.name)


class TransactionTypeMode(CommonForPreSetUp):
    mode_id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    allowed_classification = models.ManyToManyField(TransactionTypeClassification)


    def save(self, *args, **kwargs):
        if not self.mode_id:
            self.mode_id = generate_custom_id('TTM')
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.name)


# Transaction Model
class Transaction(CommonForMT):
    transaction_id = models.CharField(max_length=50, primary_key=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name="transaction_type")
    from_account_id = models.ForeignKey(Accounts, related_name="from_account_number", on_delete=models.CASCADE,
                                        null=True)
    from_currency_id = models.ForeignKey(Currency, related_name="from_currency_id", on_delete=models.CASCADE, null=True)
    from_amount = models.FloatField(blank=True, null=True)
    to_account_id = models.ForeignKey(Accounts, related_name="to_account_number", on_delete=models.CASCADE, null=True)
    to_currency_id = models.ForeignKey(Currency, related_name="to_currency_id", on_delete=models.CASCADE, null=True)
    to_amount = models.FloatField(blank=True, null=True)
    MODE = (('buy', 'Buy'), ('sell', 'Sell'), ('mid', 'Mid'), ('NoEx', 'No Exchange'))
    exchange_rate_calc_mode = models.CharField(max_length=10, choices=MODE, null=True)
    exchange_rate_used = models.ForeignKey(ExchangeRate, on_delete=models.CASCADE, null=True,
                                           related_name="exchange_rate_used", )
    transaction_type_mode = models.ForeignKey(TransactionTypeMode, related_name="txn_type_mode_txn", on_delete=models.DO_NOTHING, null=True)
    transaction_date_time = models.DateTimeField(auto_now_add=True)
    charges_applied = models.BooleanField(default=False)
    STATUS = (
        ('pending', 'pending'),
        ('success', 'success'),
        ('failed', 'failed'),
    )
    status = models.CharField(max_length=7, choices=STATUS)


    def __str__(self):
        return f"Transaction {self.transaction_id}"

    class Meta:
        # verbose_name_plural = "Transaction"
        ordering = ['-created_at']


# TransactionDetail Model
class TransactionDetail(CommonForMT):
    transaction_detail_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name="transaction")
    detail_key = models.CharField(max_length=255)
    detail_value = models.CharField(max_length=255)



    def __str__(self):
        return f"Detail {self.detail_key} for Transaction {self.transaction_id}"

    class Meta:
        verbose_name_plural = "Transaction Detail"
        ordering = ['-created_at']


# Reconciliation Model
class Reconciliation(CommonForMT):
    reconciliation_id = models.AutoField(primary_key=True)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="accounts_for_reconciliation")
    gl_file = models.BinaryField()
    matched_file = models.BinaryField()
    unmatched_file = models.BinaryField()
    date = models.DateField()
    status = models.CharField(max_length=255)



    def __str__(self):
        return f"Reconciliation {self.reconciliation_id} for Account {self.account_id}"

    class Meta:
        verbose_name_plural = "Reconciliation"
        ordering = ['-created_at']


class AccountEntry(CommonForMT):
    entry_ID = models.CharField(max_length=50, unique=True, blank=False, null=False)
    ENTRY_TYPE = (
        ('PL', 'PL'),
        ('AL', 'AL'),
    )
    # PL stands for Profit and loan and AL stands for Assets And Liabilities
    entry_type = models.CharField(max_length=2, choices=ENTRY_TYPE, null=True, blank=True)
    transaction_id = models.CharField(max_length=100)
    transaction_code = models.ForeignKey(TransactionCode, on_delete=models.CASCADE, related_name="transaction_code",
                                         null=True)
    user = models.ForeignKey('sub_part.User', on_delete=models.CASCADE, related_name="accentrys_user", null=True, blank=True)
    account_number = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="account_number_id")
    amount = models.FloatField()
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="currency_name_id", null=True)
    debit_credit_marker = models.CharField(max_length=15)


    # company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='companies_id', null=True,
    #                             editable=False)
    ref_no = models.CharField(max_length=40, null=True, editable=False)
    exposure_date = models.DateTimeField(auto_now_add=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    posting_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.transaction_id)

    class Meta:
        verbose_name_plural = "Account Entries"
        ordering = ['-entry_date']

class ServicePayment(CommonForMT):
    user = models.ForeignKey('sub_part.User', on_delete=models.CASCADE, related_name="users_id", null=True)
    debit_acc_number = models.ForeignKey(AccountHolder, on_delete=models.CASCADE,
                                         related_name="account_holder_names_dr",
                                         null=True)
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name="txn_type")
    credit_acc_number = models.ForeignKey(AccountHolder, on_delete=models.CASCADE,
                                          related_name="account_holder_names_cr",
                                          null=True)
    amount = models.FloatField()



    class Meta:
        ordering = ['-created_at']


class TellerProfile(CommonForMT):
    user = models.OneToOneField('sub_part.User', on_delete=models.CASCADE)
    cash_withdrawal_limit = models.FloatField(default=0)
    cash_deposit_limit = models.FloatField(default=0)
    currency_exchange_limit = models.FloatField(default=0)


    class Meta:
        verbose_name_plural = "Teller Profiles"
        ordering = ["-created_at"]

    def can_process_transaction(self, transaction_amount, transaction_type):
        teller_message = "The teller amount exceeded the limit"
        print('transaction_type can can_process_transaction', transaction_type)
        if 'withdrawal' in str(transaction_type) or 'payment' in str(transaction_type):
            print('its widhdf')
            print('transaction_amount ', transaction_amount)
            print('self.cash_withdrawal_limit ', self.cash_withdrawal_limit)
            return [transaction_amount <= self.cash_withdrawal_limit, teller_message]
        elif 'deposit' in str(transaction_type) or 'receipt' in str(transaction_type):
            print('its deposit..')
            return [transaction_amount <= self.cash_withdrawal_limit, teller_message]
        elif 'exchange' in transaction_type:
            return [transaction_amount <= self.cash_withdrawal_limit, teller_message]
        return [False, "Invalid transaction type. It should be one of the following: withdrawal, deposit, or exchange."]

    def clear_teller_amount(self, transaction_amount, transaction_type):
        teller_message = "The teller amount exceeded the limit"
        print('transaction_type can clear_teller_amount', transaction_type)

        if 'withdrawal' in transaction_type or 'payment' in str(transaction_type):
            if transaction_amount <= self.cash_withdrawal_limit:
                self.cash_withdrawal_limit -= transaction_amount
                self.save()
                return [True, "Withdrawal successful. Remaining limit: {}".format(self.cash_withdrawal_limit)]
            else:
                return [False, teller_message]

        elif 'deposit' in transaction_type or 'receipt' in str(transaction_type):
            if transaction_amount <= self.cash_deposit_limit:
                self.cash_deposit_limit -= transaction_amount
                self.save()
                return [True, "Deposit successful. Remaining limit: {}".format(self.cash_deposit_limit)]
            else:
                return [False, teller_message]

        elif 'exchange' in transaction_type:
            if transaction_amount <= self.currency_exchange_limit:
                self.currency_exchange_limit -= transaction_amount
                self.save()
                return [True, "Exchange successful. Remaining limit: {}".format(self.currency_exchange_limit)]
            else:
                return [False, teller_message]

        return [False, "Invalid transaction type. It should be one of the following: withdrawal, deposit, or exchange."]

    def __str__(self):
        return f'Teller: {self.user.first_name}'


# Payable, Receivable & Payment & Receipt Models

class ReferenceType(CommonForMT):
    type_id = models.CharField(max_length=10, primary_key=True)
    type_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.type_name


class PaymentComplexity(CommonForMT):
    complexity_id = models.CharField(max_length=10, primary_key=True)
    complexity_name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=250, null=True, blank=True)


    def __str__(self):
        return self.complexity_name


class AccountReceivable(CommonForMT):
    reference_type = models.ForeignKey(ReferenceType, on_delete=models.CASCADE, null=True)
    reference_number = models.CharField(max_length=50, unique=True, null=True)
    effective_from = models.DateField(null=True)
    student_name = models.CharField(max_length=255, null=True)
    student_id = models.CharField(max_length=50, null=True)
    bank = models.ForeignKey('pesanile_accounting.BankRegistration', on_delete=models.CASCADE, related_name='account_receivable_registration_code', null=True, blank=True)

    actual_amount = models.FloatField(null=True)
    payment_complexity = models.ForeignKey(PaymentComplexity, on_delete=models.CASCADE, null=True)

    payment_term_period = models.TextField(max_length=50, null=True)
    payment_term_milestone = models.TextField(max_length=255, null=True)
    payment_term_amount = models.TextField(null=True)

    amount_received = models.FloatField(default=0.00)
    amount_due = models.FloatField(default=0.00)

    due_date = models.DateField(null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)

    payment_status_choices = [
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid')
    ]
    payment_status = models.CharField(max_length=15, choices=payment_status_choices, default='unpaid')

    internal_notes = models.CharField(max_length=250, blank=True, null=True)

    customer_communication = models.CharField(max_length=250,blank=True, null=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_type} - {self.reference_number}"

class AccountPayable(CommonForMT):
    reference_type = models.ForeignKey(ReferenceType, on_delete=models.CASCADE, null=True)
    reference_number = models.CharField(max_length=50, unique=True, null=True)
    effective_from = models.DateField(null=True)

    vendor_name = models.CharField(max_length=255, null=True)
    vendor_id = models.CharField(max_length=50, null=True)

    actual_amount = models.FloatField(default=0.00)
    payment_complexity = models.ForeignKey(PaymentComplexity, on_delete=models.CASCADE, null=True)

    payment_term_period = models.TextField(max_length=50, null=True)
    payment_term_milestone = models.TextField(max_length=255, null=True)
    payment_term_amount = models.TextField(null=True)

    amount_paid = models.FloatField(default=0.00)
    amount_due = models.FloatField(default=0.00)

    due_date = models.DateField(null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True)

    payment_status_choices = [
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid')
    ]
    payment_status = models.CharField(max_length=15, choices=payment_status_choices, default='unpaid')

    internal_notes = models.CharField(max_length=250, blank=True, null=True)

    vendor_communication = models.CharField(max_length=250, blank=True, null=True)



    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_type} - {self.reference_number}"


class Payment(CommonForMT):
    account_payable = models.ForeignKey(AccountPayable, on_delete=models.CASCADE, related_name='payments')
    amount_paid = models.FloatField()
    payment_date = models.DateField()
    reference_number = models.CharField(max_length=100, unique=True)



    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.reference_number} - {self.amount_paid}"


class Receipt(CommonForMT):
    account_receivable = models.ForeignKey(AccountReceivable, on_delete=models.CASCADE, related_name='receipts')
    amount_received = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_date = models.DateField()
    reference_number = models.CharField(max_length=100, unique=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Receipt {self.reference_number} - {self.amount_received}"


class UserFinancialAccountMapping(CommonForMT):
    UFAM_ID = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255)
    user = models.ForeignKey('sub_part.User', on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('disabled', 'Disabled'),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.first_name} - {self.account}"


class UserFinancialAccountCategory(CommonForMT):
    UFAC_ID = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(AccountCategory, on_delete=models.CASCADE)
    gl_line = models.ForeignKey(GLLine, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category} - {self.gl_line}"

class AccountReceipt(CommonForMT):
    reference_type = models.ForeignKey(ReferenceType, on_delete=models.CASCADE, null=True, related_name="acc_receipt")
    transaction_id = models.CharField(max_length=50, unique=True, null=True, editable=False)
    reference_number = models.CharField(max_length=50, unique=True, null=True)
    customer_name = models.CharField(max_length=255, null=True)
    customer_id = models.CharField(max_length=50, null=True)
    amount = models.FloatField(null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, related_name="rec_currency")
    payment_status_choices = [
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'paid')
    ]
    payment_status = models.CharField(max_length=15, choices=payment_status_choices, default='paid')
    internal_notes = models.CharField(max_length=250, blank=True, null=True)
    customer_communication = models.CharField(max_length=250,blank=True, null=True)
    transaction_type_mode = models.ForeignKey(TransactionTypeMode, related_name="txn_type_mode_txn_acc_rec", on_delete=models.DO_NOTHING, null=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reference_type} - {self.reference_number}"


class AccountPayment(CommonForMT):
    reference_type = models.ForeignKey(ReferenceType, on_delete=models.CASCADE, null=True, related_name="acc_payment")
    transaction_id = models.CharField(max_length=50, unique=True, null=True, editable=False)
    reference_number = models.CharField(max_length=50, unique=True, null=True)
    vendor_name = models.CharField(max_length=255, null=True)
    vendor_id = models.CharField(max_length=50, null=True)
    amount = models.FloatField(default=0.00)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, related_name="pay_currency")
    payment_status_choices = [
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid')
    ]
    payment_status = models.CharField(max_length=15, choices=payment_status_choices, default='paid')
    internal_notes = models.CharField(max_length=250, blank=True, null=True)
    vendor_communication = models.CharField(max_length=250, blank=True, null=True)
    transaction_type_mode = models.ForeignKey(TransactionTypeMode, related_name="txn_type_mode_txn_acc_pay", on_delete=models.DO_NOTHING, null=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.reference_type} - {self.reference_number}"


class CommonRegistration(CommonForMT):
    id = models.CharField(max_length=50, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    REGISTER_AS = (
        ('item_category', 'item_category'),
        ('food', 'food'),
        ('vendor', 'vendor'),
        ('member', 'member'),
        ('employee', 'employee'),
        ('waiter', 'waiter'),
        ('product', 'product'),
    )
    register_id = models.CharField(max_length=50, null=True, blank=False)
    register_as = models.CharField(max_length=15, choices=REGISTER_AS)
    # company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="company_common_registration")

    category_type = models.ForeignKey('sacco_app.CategoryType', null=True, on_delete = models.CASCADE, related_name="category_type_cr", verbose_name= "Category Type")
    category_name = models.ForeignKey('sacco_app.Category', on_delete=models.CASCADE,
                                        related_name='category_name_cr', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.id:
            if self.register_as == 'item_category':
                prefix = 'IC'
            elif self.register_as == 'food':
                prefix = 'F'
            elif self.register_as == 'vendor':
                prefix = 'VEN'
            elif self.register_as == 'employee':
                prefix = 'EMP'
            elif self.register_as == 'waiter':
                prefix = 'WT'
            elif self.register_as == 'member':
                prefix = 'MEM'
            elif self.register_as == 'product':
                prefix = 'PRO'
            else:
                prefix='NA'
            self.id = generate_custom_id(prefix)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{str(self.name)}-{str(self.id)}"

class CustomFieldType(CommonForPreSetUp):
    cft_id = models.CharField(max_length=10, primary_key=True, editable=False)
    type_name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)


    def save(self, *args, **kwargs):
        print('args ', args)
        print('kwargs ', kwargs)
        if not self.cft_id:
            self.cft_id = generate_custom_id("CFT")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.type_name)

class CustomField(CommonForPreSetUp):
    cf_id = models.CharField(max_length=10, primary_key=True, editable=False)
    field_name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)


    def save(self, *args, **kwargs):
        print('args ', args)
        print('kwargs ', kwargs)
        if not self.cf_id:
            self.cf_id = generate_custom_id("CF")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return str(self.field_name)

class CustomTransactionFieldMapping(CommonForMT):
    ctfm_id = models.CharField(max_length=10, primary_key=True, editable=False)
    # company = models.ForeignKey(Company, on_delete = models.CASCADE, related_name='ctfm_company_name')
    transaction_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE, related_name='ctfm_txn_type')

    field_name = models.ForeignKey(CustomField, on_delete = models.CASCADE, related_name='ctfm_field_name')
    field_type = models.ForeignKey(CustomFieldType, on_delete = models.CASCADE, related_name='ctfm_field_type')
    is_required = models.BooleanField(default=False)
    identification_key = models.CharField(max_length=50, editable=False)


    def save(self, *args, **kwargs):
        print('args ', args)
        print('kwargs ', kwargs)
        if not self.ctfm_id:
            self.ctfm_id = generate_custom_id("CTFM")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.ctfm_id)

class CustomTransactionDetail(CommonForMT):
    ctd_id = models.CharField(max_length=30, primary_key=True, editable=False)
    transaction_id = models.CharField(max_length=50, null=False, blank=False)
    custom_field_id = models.ForeignKey(CustomField, on_delete=models.DO_NOTHING, related_name="ctd_cfid")
    field_value = models.CharField(max_length=250, null=True, blank=True)

    # company = models.ForeignKey(Company, on_delete=models.DO_NOTHING, related_name="ctd_company", null=True)


    def save(self, *args, **kwargs):
        print('args ', args)
        print('kwargs ', kwargs)
        if not self.ctd_id:
            self.ctd_id = generate_custom_id("CTD")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.transaction_id} || {self.custom_field_id} || {self.field_value}'
    

    
class BankRegistration(CommonForMT):
    code = models.CharField(max_length=100, unique=True)
    bank_name = models.CharField(max_length=100, unique=True)
    description = models.TextField()


    def __str__(self):
        return f"{self.code} - {self.bank_name}"

# AccountType Model
class BusinessGroup(CommonForPreSetUp):
    business_group_id = models.CharField(max_length=10, primary_key=True, editable=False)
    name = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.business_group_id:
            self.business_group_id = generate_custom_id('BG')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Business Group"
        ordering = ['-created_at']

class Department(CommonForPreSetUp):
    dept_id = models.CharField(max_length=50, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Department Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    business_group = models.ForeignKey('BusinessGroup',on_delete=models.CASCADE,related_name='departments',verbose_name="Business Group")

    def save(self, *args, **kwargs):
        if not self.dept_id:
            self.dept_id = generate_custom_id('DPT')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['name']

    def __str__(self):
        return self.name
