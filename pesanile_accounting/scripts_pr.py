# from django.db import transaction
# from django.utils import timezone
# from .models import *
# import datetime  # Import datetime module
#
#
# def apply_payment_to_receivable(reference_number, payment_amount,company_id=None,branch=None):
#     """
#     Applies a payment to the receivable, updates the amount due, amount received,
#     and payment status, and records the last payment date.
#     """
#     try:
#         receivable = AccountReceivable.objects.get(reference_number=reference_number)
#     except AccountReceivable.DoesNotExist:
#         return [False, f"Invalid Reference Number : {reference_number}"] # Handle the case where the receivable does not exist
#         # Ensure that the payment amount does not exceed the amount due
#     if payment_amount > receivable.amount_due:
#         print('reference_number ',reference_number)
#         print('payment_amount ',payment_amount)
#         print('receivable.amount_due ',receivable.amount_due)
#         extra_amount = payment_amount - receivable.amount_due
#         payment_amount = receivable.amount_due
#         print('extra_amount ', extra_amount)
#         return [False, f"System will not accept more than the due amount, Due Amount is : {payment_amount}"]
#     with transaction.atomic():
#         receivable.amount_received += payment_amount
#         receivable.amount_due = receivable.actual_amount - receivable.amount_received
#         receivable.last_payment_date = timezone.now().date()
#
#         if receivable.amount_due <= 0:
#             receivable.payment_status = 'Paid'
#             receivable.amount_due = 0  # To prevent negative amounts
#         elif receivable.amount_received > 0:
#             receivable.payment_status = 'Partially Paid'
#         else:
#             receivable.payment_status = 'Unpaid'
#
#         receivable.save()
#         # Optionally, create a Receipt record
#         obj = Receipt.objects.create(
#             account_receivable=receivable,
#             amount_received=payment_amount,
#             receipt_date=timezone.now().date(),
#             reference_number=f'REC{int(timezone.now().timestamp())}',
#             company_name=company_id,
#             branch_name=branch,
#         )
#
#     return [True, receivable]
#
#
# def apply_payment_to_payable(reference_number, payment_amount,company_id=None,branch=None):
#     try:
#         # Fetch the AccountPayable instance
#         account_payable = AccountPayable.objects.get(reference_number=reference_number)
#     except AccountPayable.DoesNotExist:
#         return [False, f"Invalid Reference Number : {reference_number}"]
#
#     # Ensure that the payment amount does not exceed the amount due
#     if payment_amount > account_payable.amount_due:
#         extra_amount = payment_amount - account_payable.amount_due
#         payment_amount = account_payable.amount_due
#         print('extra_amount ', extra_amount)
#         return [False, f"System will not accept more than the due amount, Due Amount is : {payment_amount}"]
#
#     with transaction.atomic():
#         # Update Amount Paid and Amount Due
#         account_payable.amount_paid += payment_amount
#         account_payable.amount_due = max(account_payable.actual_amount - account_payable.amount_paid, 0)
#
#         # Update Payment Status
#         if account_payable.amount_due <= 0:
#             account_payable.payment_status = 'paid'
#             account_payable.amount_due = 0
#         elif account_payable.amount_paid > 0:
#             account_payable.payment_status = 'partially_paid'
#         else:
#             account_payable.payment_status = 'unpaid'
#
#         # Update Last Payment Date
#         account_payable.last_payment_date = datetime.date.today()
#
#         # Save the updated AccountPayable
#         account_payable.save()
#
#         # Create a Payment record
#         payment = Payment.objects.create(
#             account_payable=account_payable,
#             amount_paid=payment_amount,
#             payment_date=datetime.date.today(),
#             reference_number=f'PAY{int(datetime.datetime.now().timestamp())}',
#             company_name = company_id,
#             branch_name = branch,
#         )
#         print('payment ', payment)
#
#     return [True, account_payable]
#
# def get_receivable_and_payable_details(reference_number,transaction_type_name):
#     try:
#         transaction_type_name = str(transaction_type_name).lower()
#         if transaction_type_name == 'receipt':
#             obj = AccountReceivable.objects.get(reference_number=reference_number)
#             return  [True, obj]
#         if transaction_type_name == 'payment':
#             obj = AccountPayable.objects.get(reference_number=reference_number)
#             return  [True, obj]
#     except Exception as error:
#         return [False, f"""{error}"""]
#


from django.db import transaction
from django.utils import timezone
from .models import *
import datetime  # Import datetime module

def receivable_atomic(reference_number,payment_amount,company_id=None,branch=None):
    try:
        receivable = AccountReceivable.objects.get(reference_number=reference_number)
    except AccountReceivable.DoesNotExist:
        return [False, f"Invalid Reference Number : {reference_number}"] # Handle the case where the receivable does not exist
        # Ensure that the payment amount does not exceed the amount due
    with transaction.atomic():
        # receivable.amount_received += payment_amount
        # receivable.amount_due = receivable.actual_amount - receivable.amount_received
        # receivable.last_payment_date = timezone.now().date()

        if receivable.amount_due <= 0:
            receivable.payment_status = 'paid'
            receivable.amount_due = 0  # To prevent negative amounts
        elif receivable.amount_received > 0:
            receivable.payment_status = 'partially_paid'
        else:
            receivable.payment_status = 'unpaid'

        receivable.save()

        receipt_obj = Receipt.objects.create(
            account_receivable=receivable,
            amount_received=payment_amount,
            receipt_date=timezone.now().date(),
            reference_number=f'REC{int(timezone.now().timestamp())}',
            # company_name=company_id,
            # branch_name=branch,
        )
    return receivable
def apply_payment_to_receivable(reference_number, payment_amount,company_id=None,branch=None):
    """
    Applies a payment to the receivable, updates the amount due, amount received,
    and payment status, and records the last payment date.
    """
    try:
        receivable = AccountReceivable.objects.get(reference_number=reference_number)
    except AccountReceivable.DoesNotExist:
        return [False, f"Invalid Reference Number : {reference_number}"] # Handle the case where the receivable does not exist
        # Ensure that the payment amount does not exceed the amount due
    if payment_amount > receivable.amount_due:
        print('reference_number ',reference_number)
        print('payment_amount ',payment_amount)
        print('receivable.amount_due ',receivable.amount_due)
        extra_amount = payment_amount - receivable.amount_due
        payment_amount = receivable.amount_due
        print('extra_amount ', extra_amount)
        return [False, f"System will not accept more than the due amount, Due Amount is : {payment_amount}"]

        # Optionally, create a Receipt record

    return [True, receivable]

def payment_atomic(reference_number,payment_amount,company_id=None,branch=None):
    try:
        # Fetch the AccountPayable instance
        account_payable = AccountPayable.objects.get(reference_number=reference_number)
    except AccountPayable.DoesNotExist:
        return [False, f"Invalid Reference Number : {reference_number}"]
    with transaction.atomic():
        # Update Amount Paid and Amount Due
        account_payable.amount_paid += payment_amount
        account_payable.amount_due = max(account_payable.actual_amount - account_payable.amount_paid, 0)

        # Update Payment Status
        if account_payable.amount_due <= 0:
            account_payable.payment_status = 'paid'
            account_payable.amount_due = 0
        elif account_payable.amount_paid > 0:
            account_payable.payment_status = 'partially_paid'
        else:
            account_payable.payment_status = 'unpaid'

        # Update Last Payment Date
        account_payable.last_payment_date = datetime.date.today()

        # Save the updated AccountPayable
        account_payable.save()

        # Create a Payment record
        payment = Payment.objects.create(
            account_payable=account_payable,
            amount_paid=payment_amount,
            payment_date=datetime.date.today(),
            reference_number=f'PAY{int(datetime.datetime.now().timestamp())}',
            # company_name = company_id,
            # branch_name = branch,
        )
    return account_payable

def apply_payment_to_payable(reference_number, payment_amount,company_id=None,branch=None):
    try:
        # Fetch the AccountPayable instance
        account_payable = AccountPayable.objects.get(reference_number=reference_number)
    except AccountPayable.DoesNotExist:
        return [False, f"Invalid Reference Number : {reference_number}"]

    # Ensure that the payment amount does not exceed the amount due
    if payment_amount > account_payable.amount_due:
        extra_amount = payment_amount - account_payable.amount_due
        payment_amount = account_payable.amount_due
        print('extra_amount ', extra_amount)
        return [False, f"System will not accept more than the due amount, Due Amount is : {payment_amount}"]

    return [True, account_payable]

def get_receivable_and_payable_details(reference_number,transaction_type_name):
    try:
        transaction_type_name = str(transaction_type_name).lower()
        if transaction_type_name == 'receipt':
            obj = AccountReceivable.objects.get(reference_number=reference_number)
            return  [True, obj]
        if transaction_type_name == 'payment':
            obj = AccountPayable.objects.get(reference_number=reference_number)
            return  [True, obj]
    except Exception as error:
        return [False, f"""{error}"""]

