from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

from sub_part.models import User,Company,Branch
from .models import *
from django.db.models.signals import pre_save, post_save
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib import messages
from pesanile_accounting.scripts import *
from sacco_app.models import DefaultAccountSetUp


@receiver(user_logged_in, sender=User)
def user_logged_in_success(sender, request, user, *args, **kwargs):
    print('user logged in success')
    print('sender ', sender)
    print('request ', request)
    print('sender ', user)
    print('#' * 30)
    # write other logic


@receiver(user_logged_out, sender=User)
def user_logged_out_success(sender, request, user, *args, **kwargs):
    print('user logged out success')
    print('sender ', sender)
    print('request ', request)
    print('sender ', user)
    print('#' * 30)
    # write other logic


@receiver(user_login_failed)
def user_login_failed(sender, credentials, *args, **kwargs):
    print('user login failed')
    print('sender ', sender)
    print('credentials ', credentials)
    print('#' * 30)
    # write other logic


# @receiver(pre_save, sender=Accounts)
# def accounts_pre_save(sender, instance, *args, **kwargs):
#     print(args)
#     print(kwargs)
#     print(sender, instance)
#     print('Instance ', instance.account_number)
#     if instance.account_number == '':
#         account_count = Accounts.objects.all().count()
#         print('account_count ==> ', account_count)
#         instance.account_number = generate_account_number(last_serial_number=account_count, number_of_digits='06')
#         print("instance.account_number :- ", instance.account_number)


# @receiver(post_save, sender=Accounts)
# def accounts_post_save(sender, instance, created, *args, **kwargs):
#     try:
#         print(args)
#         print(kwargs)
#         print(sender, instance)
#         print('created ', created)
#         if created:
#             print('successfully saved...')
#         else:
#             print('its Exists')
#     except ValidationError:
#         pass

@receiver(post_save, sender=Company)
def company_post_save(sender, instance, created, *args, **kwargs):
    try:
        print(args)
        print(kwargs)
        print(sender, instance)
        print('created ', created)
        if created:
            try:
                assets_type = ['Liability', 'Expense', 'Income', 'Cashbook']
                account_type = ['Liability', 'Expense', 'Income', 'Cashbook']
                account_category = ['Liability', 'Expense', 'Income', 'Cashbook']
                for assets_type, account_type, account_category in zip(assets_type, account_type, account_category):
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
                                                    account_type=acc_type_obj, company=instance,base_currency=instance.local_currency)
                    print('acc_obj ', acc_obj)
            except Exception as error:
                print('signal.py file || Creating Account its raising error ',error)
        else:
            print('its Exists')
    except Exception as error:
        print('error ==> ',error)



@receiver(post_save, sender=CommonRegistration)
def common_registration_post_save(sender, instance, created, *args, **kwargs):
    try:
        print(args)
        print(kwargs)
        print(sender, instance)
        print('created ', created)
        if created:
            try:
                assets_type = ['Liability', 'Expense', 'Income']
                account_type = ['Liability', 'Expense', 'Income']
                account_category = ['Liability', 'Expense', 'Income']
                if instance.register_as == 'item_category':
                    assets_type = ['Liability', 'Expense', 'Income']
                    account_type = ['Liability', 'Expense', 'Income']
                    account_category = ['Liability', 'Expense', 'Income']
                elif instance.register_as == 'food':
                    assets_type = ['Liability', 'Expense', 'Income']
                    account_type = ['Liability', 'Expense', 'Income']
                    account_category = ['Liability', 'Expense', 'Income']
                elif instance.register_as == 'vendor':
                    assets_type = ['Liability', 'Expense', 'Income']
                    account_type = ['Liability', 'Expense', 'Income']
                    account_category = ['Liability', 'Expense', 'Income']
                elif instance.register_as == 'employee':
                    assets_type = ['Liability', 'Expense',]
                    account_type = ['Liability', 'Expense', ]
                    account_category = ['Liability', 'Expense', ]
                elif instance.register_as == 'waiter':
                    assets_type = ['Liability', 'Expense', 'Income']
                    account_type = ['Liability', 'Expense', 'Income']
                    account_category = ['Liability', 'Expense', 'Income']

                elif instance.register_as == 'member' or instance.register_as == 'product':
                    category_name = instance.category_name
                    category_type = instance.category_type
                    company = instance.company
                    register_as = instance.register_as
                    register_id = instance.register_id
                    id = instance.id
                    print('category_name ',category_name)
                    print('category_type ',category_type)
                    obj = DefaultAccountSetUp.objects.filter(Q(category_name_id=category_name)&Q(category_type_id=category_type))
                    print('obj ',obj.count())
                    for data in obj:
                        account_count = Accounts.objects.all().count()
                        acc_nub_glline = generate_account_number(last_serial_number=account_count,
                                                                 number_of_digits='06')
                        acc_obj = create_or_get_account(acc_nub_glline, gl_line=data.glline,
                                                        account_category=data.account_category,
                                                        account_type=data.account_type,
                                                        base_currency=instance.company.local_currency, cr_id=instance)
                        print('acc_obj ',acc_obj)
                    return
                for assets_type, account_type, account_category in zip(assets_type, account_type, account_category):
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
                                                    account_type=acc_type_obj, base_currency=instance.company.local_currency, cr_id=instance)
                    print('acc_obj ',acc_obj)
            except Exception as error:
                print('signal.py file || Creating Account its raising error ',error)
        else:

            print('its Exists')
    except Exception as error:
        print('error ==> ',error)


@receiver(post_save, sender=BankRegistration)
def bank_post_save(sender, instance, created, *args, **kwargs):
    try:
        print(args)
        print(kwargs)
        print(sender, instance)
        print('created ', created)
        if created:
            try:
                assets_type = ['Cashbook']
                account_type = ['Cashbook']
                account_category = ['Cashbook']
                for assets_type, account_type, account_category in zip(assets_type, account_type, account_category):
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
                                                    account_type=acc_type_obj, bank=instance)
                    print('acc_obj ', acc_obj)
            except Exception as error:
                print('signal.py file || Creating Account its raising error ',error)
        else:
            print('its Exists')
    except Exception as error:
        print('error ==> ',error)
