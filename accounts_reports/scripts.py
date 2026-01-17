from pesanile_accounting.models import AccountEntry, User, Accounts

from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date


def date_wise_report(start_date=None, end_date=None):
    try:
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)

        if not start_date and not end_date:
            return AccountEntry.objects.all()

        if start_date and end_date:
            return AccountEntry.objects.filter(entry_date__range=[start_date, end_date])
        elif start_date:
            return AccountEntry.objects.filter(entry_date__gte=start_date)
        elif end_date:
            return AccountEntry.objects.filter(entry_date__lte=end_date)

    except ValueError:
        # Handle invalid date format
        print("Invalid date format provided")
        return AccountEntry.objects.none()


def transaction_id_wise_report(transaction_id):
    try:
        print("its coming",transaction_id)
        return AccountEntry.objects.filter(transaction_id=transaction_id.strip())

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()


def account_wise_report(account_number):
    try:
        return AccountEntry.objects.filter(account_number=account_number)

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()

def TJ_wise_report(account_number,start_date,end_date):
    try:
        if start_date:
            start_date = parse_date(start_date)
        if end_date:
            end_date = parse_date(end_date)
        print("account_number",account_number)
        acc_entry = AccountEntry.objects.filter(entry_date__range=[start_date, end_date])
        if account_number:
            acc_entry=acc_entry.filter(account_number=account_number)
        return acc_entry

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()


def teller_wise_report(user_id):
    try:
        return AccountEntry.objects.filter(user_id=user_id)

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()


def transaction_code_wise_report(txn_code):
    try:
        return AccountEntry.objects.filter(transaction_code_id=txn_code)

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()



def till_wise_report(till_code):
    try:
        return AccountEntry.objects.filter(ref_no=till_code)

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()

def dutymeal_wise_report(dutymeal_id):
    try:
        return AccountEntry.objects.filter(ref_no=dutymeal_id)

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()
    
def company_wise_report(company_id):
    try:
        obj = User.objects.filter(company_name_id=str(company_id))
        print('obj ', obj)
        user_list = [data.pk for data in obj]
        print('user_list ', user_list)
        return AccountEntry.objects.filter(user_id__in=user_list)

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()


def glline_with_different_sub_glline_wise_report(glline):
    try:
        print('glline ',glline)
        obj = Accounts.objects.filter(gl_line_id=str(glline))
        print('obj ', obj)
        obj_list = [data.pk for data in obj]
        print('obj_list ', obj_list)
        return AccountEntry.objects.filter(account_number_id__in=obj_list)

    except ValueError:
        # Handle invalid date format
        print("Invalid")
        return AccountEntry.objects.none()
