from .models import Accounts, AccountEntry
import random
import string
from datetime import date
from django.utils.crypto import get_random_string


def account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount, credit_currency=None,
                  total_debit_amt=0, debit_currency=None,
                  dr_acc=None,
                  cr_acc=None,
                  debit_credit_marker='DebitCredit', user=None, company=None,ref_no=None,branch=None):
    """
    Here, total_debit_amt is mandatory when debit credit marker will be DebitCredit
    total_debit_amt should be total amount of transaction
    amount should be split amount in case total_debit_amt is 500 and 200 will be any service charge and 300 will be other charges
    so
    total_debit_amt = 500
    amount = 200
    amount = 300
    """
    print('company ',company)
    print('branch ',branch)
    try:
        entry_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        print('Account Entry Statement ...')
        print(' credit_currency ', credit_currency)
        print(' debit_currency  ', debit_currency)
        print(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount, total_debit_amt, dr_acc, cr_acc,
              user)
        if debit_credit_marker == "DebitCredit":
            # ================Debit account Process Start======================
            print(type(dr_acc))
            dr_acc_detail = Accounts.objects.get(account_id=dr_acc)
            print('here ', dr_acc_detail)
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code=dr_txn_code,
                user_id=user,
                account_number_id=dr_acc,
                amount=-float(total_debit_amt),
                currency_id=debit_currency,
                # company_name=company,
                # branch_name=branch,
                ref_no=ref_no,
                debit_credit_marker='Debit',
            )
            dr_acc_detail.current_cleared_balance = dr_acc_detail.current_cleared_balance - float(total_debit_amt)
            dr_acc_detail.total_balance = dr_acc_detail.total_balance - float(total_debit_amt)
            dr_acc_detail.save()
            print('Credit process.')
            # ================Debit account Process End========================

            # ================Credit Account Process Start=====================
            entry_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            cr_acc_detail = Accounts.objects.get(account_id=str(cr_acc))
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code=cr_txn_code,
                user_id=user,
                account_number_id=cr_acc,
                amount=+float(credit_amount),
                currency_id=credit_currency,
                
                ref_no=ref_no,
                debit_credit_marker='Credit',
            )
            print('here...')
            cr_acc_detail.current_cleared_balance = cr_acc_detail.current_cleared_balance + float(credit_amount)
            cr_acc_detail.total_balance = cr_acc_detail.total_balance + float(credit_amount)
            cr_acc_detail.save()
            # ================Credit Account Process End=======================
            return True
        elif debit_credit_marker == 'Debit':
            # ================Debit account Process Start======================
            print(type(dr_acc))
            dr_acc_detail = Accounts.objects.get(account_id=dr_acc)
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code=dr_txn_code,
                user_id=user,
                account_number_id=dr_acc,
                amount=-float(total_debit_amt),
                currency_id=debit_currency,
               
                ref_no=ref_no,
                debit_credit_marker='Debit',
            )
            dr_acc_detail.current_cleared_balance = dr_acc_detail.current_cleared_balance - float(total_debit_amt)
            dr_acc_detail.total_balance = dr_acc_detail.total_balance - float(total_debit_amt)
            dr_acc_detail.save()
            print('Credit process.')
            # ================Debit account Process End========================
            return True
        elif debit_credit_marker == 'Credit':
            # ================Credit Account Process Start=====================
            entry_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            cr_acc_detail = Accounts.objects.get(account_id=str(cr_acc))
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code=cr_txn_code,
                user_id=user,
                account_number_id=cr_acc,
                amount=+float(credit_amount),
                currency_id=credit_currency,
                company_name=company,
             
                ref_no=ref_no,
                debit_credit_marker='Credit',
            )
            print('here...')
            cr_acc_detail.current_cleared_balance = cr_acc_detail.current_cleared_balance + float(credit_amount)
            cr_acc_detail.total_balance = cr_acc_detail.total_balance + float(credit_amount)
            cr_acc_detail.save()
            # ================Credit Account Process End=======================
            return True
        else:
            print('Account Entries :- debit_credit_marker not matched...')
            return False
    except Exception as error:
        print('error ', error)
        return False



def account_entry1(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount, credit_currency=None,
                  total_debit_amt=0, debit_currency=None,
                  dr_acc=None,
                  cr_acc=None,
                  debit_credit_marker='DebitCredit', user=None, company=None,ref_no=None):
    """
    Here, total_debit_amt is mandatory when debit credit marker will be DebitCredit
    total_debit_amt should be total amount of transaction
    amount should be split amount in case total_debit_amt is 500 and 200 will be any service charge and 300 will be other charges
    so
    total_debit_amt = 500
    amount = 200
    amount = 300
    """
    try:
        entry_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
        print('Account Entry Statement ...')
        print(' credit_currency ', credit_currency)
        print(' debit_currency  ', debit_currency)
        print(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount, total_debit_amt, dr_acc, cr_acc,
              user)
        if debit_credit_marker == "DebitCredit":
            # ================Debit account Process Start======================
            print(type(dr_acc))
            dr_acc_detail = Accounts.objects.get(account_id=dr_acc)
            print('here ', dr_acc_detail)
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code_id=dr_txn_code,
                user_id=user,
                account_number_id=dr_acc,
                amount=+float(total_debit_amt),
                currency_id=debit_currency,
                company_name=company,
                branch_name=branch,
                ref_no=ref_no,
                debit_credit_marker='Credit',
            )
            dr_acc_detail.current_cleared_balance = dr_acc_detail.current_cleared_balance + float(total_debit_amt)
            dr_acc_detail.total_balance = dr_acc_detail.total_balance + float(total_debit_amt)
            dr_acc_detail.save()
            print('Credit process.')
            # ================Debit account Process End========================

            # ================Credit Account Process Start=====================
            entry_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            cr_acc_detail = Accounts.objects.get(account_id=str(cr_acc))
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code_id=cr_txn_code,
                user_id=user,
                account_number_id=cr_acc,
                amount=-float(credit_amount),
                currency_id=credit_currency,
                company_name=company,
                branch_name=branch,
                ref_no=ref_no,
                debit_credit_marker='Debit',
            )
            print('here...')
            cr_acc_detail.current_cleared_balance = cr_acc_detail.current_cleared_balance - float(credit_amount)
            cr_acc_detail.total_balance = cr_acc_detail.total_balance - float(credit_amount)
            cr_acc_detail.save()
            # ================Credit Account Process End=======================
            return True
        elif debit_credit_marker == 'Debit':
            # ================Debit account Process Start======================
            print(type(dr_acc))
            dr_acc_detail = Accounts.objects.get(account_id=dr_acc)
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code_id=dr_txn_code,
                user_id=user,
                account_number_id=dr_acc,
                amount=+float(total_debit_amt),
                currency_id=debit_currency,
                company_name=company,
                branch_name=branch,
                ref_no=ref_no,
                debit_credit_marker='Credit',
            )
            dr_acc_detail.current_cleared_balance = dr_acc_detail.current_cleared_balance + float(total_debit_amt)
            dr_acc_detail.total_balance = dr_acc_detail.total_balance + float(total_debit_amt)
            dr_acc_detail.save()
            print('Credit process.')
            # ================Debit account Process End========================
            return True
        elif debit_credit_marker == 'Credit':
            # ================Credit Account Process Start=====================
            entry_id = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            cr_acc_detail = Accounts.objects.get(account_id=str(cr_acc))
            AccountEntry.objects.create(
                entry_ID=entry_id,
                entry_type=entry_type,
                transaction_id=transaction_id,
                transaction_code_id=cr_txn_code,
                user_id=user,
                account_number_id=cr_acc,
                amount=-float(credit_amount),
                currency_id=credit_currency,
                company_name=company,
                branch_name=branch,
                ref_no=ref_no,
                debit_credit_marker='Debit',
            )
            print('here...')
            cr_acc_detail.current_cleared_balance = cr_acc_detail.current_cleared_balance - float(credit_amount)
            cr_acc_detail.total_balance = cr_acc_detail.total_balance - float(credit_amount)
            cr_acc_detail.save()
            # ================Credit Account Process End=======================
            return True
        else:
            print('Account Entries :- debit_credit_marker not matched...')
            return False
    except Exception as error:
        print('error ', error)
        return False
