from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from .models import *
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib import messages
from pesanile_accounting.scripts import *
from loan_app.models import LoanRegistration


@receiver(post_save, sender=LoanRegistration)
def common_registration_post_save(sender, instance, created, *args, **kwargs):
    try:
        print(args)
        print(kwargs)
        print(sender, instance)
        print('created ', created)
        if created:
            try:
                accounts = ['Loan', 'Repayment', 'Penalty','Interest','Disbursement','Milestone']
                assets_type = ['Current Liability', 'Current Asset', 'Income','Income','Current Asset/Expense', 'Current Asset/Expense']
                account_type = ['Liability', 'Asset', 'Revenue','Revenue','Expense','Expense/Asset']
                account_category = ['Loan', 'Cash/Bank', 'Penalty Fees/Income','Interest Income','Loan Disbursement','Milestones']

                for accounts, assets_type, account_type, account_category in zip(accounts,assets_type, account_type, account_category):
                    account_count = Accounts.objects.all().count()
                    acc_nub_glline = generate_account_number(last_serial_number=account_count,
                                                                      number_of_digits='06')
                    print('acc_nub_glline ',acc_nub_glline)
                    asset_obj = create_or_get_asset_type(assets_type, assets_type)
                    print('asset_obj ', asset_obj)
                    glline_obj = create_or_get_gl_line(acc_nub_glline, account_type, account_type, asset_type=asset_obj)
                    print('glline_obj ', glline_obj)
                    acc_type_obj = create_or_get_account_type(account_type, account_type)
                    print('acc_type_obj ', acc_type_obj)
                    acc_cat_obj = create_or_get_account_category(account_category, account_category)
                    print('acc_cat_obj ', acc_cat_obj)
                    acc_obj = create_or_get_account(acc_nub_glline, gl_line=glline_obj, account_category=acc_cat_obj,
                                                    account_type=acc_type_obj, base_currency=None, cr_id=None,loan_id=instance)
                    print('acc_obj ',acc_obj)
            except Exception as error:
                print('signal.py file || Creating Account its raising error ',error)
        else:

            print('its Exists')
    except Exception as error:
        print('error ==> ',error)

