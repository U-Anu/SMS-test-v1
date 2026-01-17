from django.contrib.auth.models import User
from .models import *
import uuid
from django.db import transaction
import random
import string
from django.db.models import F
from django.contrib.auth import get_user_model
from pesanile_accounting import *
import logging
from django.core.exceptions import ObjectDoesNotExist
from pesanile_accounting.models import Accounts as Accounts,AccountType as AccountTypes,GLLine as GLLines,AccountCategory as AccountCategory
logger = logging.getLogger(__name__)


def create_student_account(student_instance):
    try:
        print("====student_instance",student_instance)
        # Get or create AccountType
        account_type, created = AccountType.objects.get_or_create(
            name="Student Account Type",
            defaults={
                "abbreviation": "...",  # Replace with actual value
                "description": "...",  # Replace with actual value
            },
        )
        print("====acc",account_type)
        # Get or create GLLine for schools
        gl_line = GLLine.get_school_gl_line()
        print("====gl",gl_line)
        # Get or create the GLLine record for schools
        school_gl_line, created = GLLine.objects.get_or_create(
            short_description="School GL Line",
            defaults={
                "description": "GL Line for schools",
                "status": "active",
                "current_cleared_balance": 0,
                "current_uncleared_balance": 0,
                "total_balance": 0,
            },
        )
        print("****school_gl_line",school_gl_line)
        # Ensure that the GLLine record was either retrieved or created
        assert not created, "Failed to get or create GLLine for schools"
        if account_type and gl_line:
            # Customize the account number format
            account_number = f"STU-{student_instance.id}"
            account_description = f"Student Account for {student_instance.first_name} {student_instance.last_name}"

            # Create the corresponding Account
            account = Account.objects.create(
                account_type=account_type,
                gl_line_number=gl_line,
                account_number=account_number,
                account_description=account_description,
                user=User.objects.get(pk=student_instance.user_student_id),
                opening_balance=0,
                current_cleared_balance=0,
                current_uncleared_balance=0,
                total_balance=0,
            )

            return account

    except ObjectDoesNotExist as does_not_exist_error:
        logger.error(f"Object does not exist error: {does_not_exist_error}")
        print(f"Object does not exist error: {does_not_exist_error}")
    except Exception as error:
        logger.error(f"Error in create_student_account: {error}")
        print(f"Error in create_student_account: {error}")

    return None


# accounts.py

from django.db import transaction


logger = logging.getLogger(__name__)


def create_school_account(school_instance,branch_id):
    try:
        # Get or create AccountType for schools
        account_type, created = AccountType.objects.get_or_create(
            name="School Account Type",
            defaults={
                "abbreviation": f"SCH-{school_instance.id}",  # Customize the abbreviation as needed
                "description": f"Account Type for {school_instance.name}",
            },
        )

        # Get or create GLLine for schools
        school_gl_line, created = GLLine.objects.get_or_create(
            short_description="School GL Line",
            defaults={
                "description": "GL Line for schools",
                "status": "active",
                "current_cleared_balance": 0,
                "current_uncleared_balance": 0,
                "total_balance": 0,
            },
        )

        # Ensure that the GLLine record was either retrieved or created
        assert not created, "Failed to get or create GLLine for schools"

        if account_type and school_gl_line:
            # Use the school's method to get or generate the account number
            account_number = school_instance.get_or_generate_account_number()

            account_description = f"School Account for {school_instance.name}"

            # Create the corresponding Account
            account = Account.objects.create(
                account_type=account_type,
                gl_line_number=school_gl_line,
                account_number=account_number,
                account_description=account_description,
                user=User.objects.get(pk=school_instance.admin_in_charge_id),
                opening_balance=0,
                current_cleared_balance=0,
                current_uncleared_balance=0,
                total_balance=0,
                branch_id=branch_id
            )

            return account

    except ObjectDoesNotExist as does_not_exist_error:
        logger.error(f"Object does not exist error: {does_not_exist_error}")
        print(f"Object does not exist error: {does_not_exist_error}")
    except Exception as error:
        logger.error(f"Error in create_school_account: {error}")
        print(f"Error in create_school_account: {error}")

    return None


from django.db import transaction


@transaction.atomic
def account_creation(pre_fix, account_type_name, account_description, user_id):
    try:
        print("Check ", pre_fix, account_type_name, account_description, user_id)
        get_acc = get_acc_no(pre_fix)

        # Use get_or_create to handle the case where the AccountType doesn't exist
        get_acc_type, created = AccountType.objects.get_or_create(
            name=account_type_name
        )
        acc_type_id = get_acc_type.id

        print("get_acc ", get_acc)
        print("acc_type_id ", acc_type_id)

        # Create the Account instance
        account_instance = Account.objects.create(
            account_type_id=acc_type_id,
            account_number=get_acc,
            account_description=account_description,
            user_id=user_id,
        )

        return account_instance
    except AccountType.DoesNotExist:
        print(f"AccountType with name '{account_type_name}' does not exist.")
    except Exception as error:
        print("account_creation function error ", error)

    return None


def account_entry(member_id, group_id, pay_amount, dr_acc, cr_acc, transaction_id):
    try:
        # Generate a unique entry_ID using UUID
        entry_id = str(uuid.uuid4())

        # account entry logic here
        entry = AccountEntry.objects.create(
            entry_ID=entry_id,
            entry_type="PL",  # Set the appropriate entry type here
            transaction_ID=transaction_id,
            user_id=user_id,  # Replace with the actual user instance if available
            account_number=None,  # Replace with the actual Account instance
            amount=pay_amount,
            currency="KES",  # Set the appropriate currency
            debit_credit_marker="DR",  # Set the appropriate marker
            # You may need to adjust the fields based on your actual requirements
        )

        # Additional logic or validations can be added here

        success = True
    except Exception as e:
        # Log the exception or handle it based on your requirements
        print(f"Error in account entry: {e}")
        success = False

    return success


# collect school fees
def collect_school_fees(records_id, fee_amount, user_id):
    try:
        # Ensure that student.account is an instance of Account
        # if not isinstance(student.account, Account):
        #     raise ValueError(f"Invalid account type for student {student.id}")
        student = StudentAdmission.objects.get(id=records_id)
        # school = School.objects.get(id=school.id)
        # Get the User instance for the user_id
        user = User.objects.get(id=user_id)
        # Generate unique entry IDs
        entry_id_student = "".join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )
        entry_id_school = "".join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )
        income_transaction_type = TransactionType.objects.get(
            short_description="Income Transaction Type"
        )

        # Debit the student's account
        AccountEntry.objects.create(
            entry_ID=entry_id_student,
            entry_type="PL",  # You can adjust this based on your Entry Type choices
            transaction_ID=f"FEES_{student.id}",
            # user=student.id,
            # user_id=student.id
            user_id=student.id,
            student_account=student.account,
            amount=-fee_amount,
            currency="KES",
            debit_credit_marker="Debit",
        )
        print("server running")
        print(student.account)

        # Credit the school's account
        AccountEntry.objects.create(
            entry_ID=entry_id_school,
            entry_type="PL",  # adjust this based on your Entry Type choices
            transaction_ID=f"FEES_{student.id}",
            created_by=user,
            school_account=student.school.account,  # school has an 'account' field
            amount=fee_amount,
            currency="KES",
            debit_credit_marker="Credit",
            transaction_type=income_transaction_type,
        )
        print("server running")
        print(student.school.account)
        # Update the account balances
        Account.objects.filter(account_number=student.account).update(
            current_cleared_balance=F("current_cleared_balance") - fee_amount,
            total_balance=F("total_balance") - fee_amount,
        )

        Account.objects.filter(account_number=student.school.account).update(
            current_cleared_balance=F("current_cleared_balance") + fee_amount,
            total_balance=F("total_balance") + fee_amount,
        )

        return True
    except Exception as error:
        print("Error in collect_school_fees:", error)
    return False  # collect income


# collect income
def collect_income(income_instance, user_id):
    try:
        # Generate unique entry ID
        entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        user = User.objects.get(id=user_id)

        # Retrieve the user's school
        user_school = user.school

        if user_school is None:
            # Handle the case when user's school is None
            print("Error in collect_expense: User's school is None")
            return False
        income_transaction_type = TransactionType.objects.get(
            short_description="Income Transaction Type"
        )

        # Retrieve the school's account
        school_account = user_school.account

        if school_account is None:
            # Handle the case when school_account is None
            print("Error in collect_expense: School's account is None")
            return False

        # Credit the school's account for expense
        AccountEntry.objects.create(
            entry_ID=entry_id,
            entry_type="PL",
            user=user,
            school_account=school_account,
            amount=income_instance.amount,
            currency="KES",
            debit_credit_marker="Credit",
            transaction_type=income_transaction_type,
        )

        # Update the school's balance amount
        Account.objects.filter(account_number=school_account.account_number).update(
            current_cleared_balance=F("current_cleared_balance")
            + income_instance.amount,
            total_balance=F("total_balance") + income_instance.amount,
        )
        return True
    except Exception as error:
        print("Error in collect_expense:", error)
        return False


# collect expense
def collect_expense(expense_instance, user_id):
    try:
        # Generate unique entry ID
        entry_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        user = User.objects.get(id=user_id)
        expense_transaction_type = TransactionType.objects.get(
            short_description="Expense Transaction Type"
        )

        # Retrieve the user's school
        user_school = user.school

        if user_school is None:
            # Handle the case when user's school is None
            print("Error in collect_expense: User's school is None")
            return False

        # Retrieve the school's account
        school_account = user_school.account

        if school_account is None:
            # Handle the case when school_account is None
            print("Error in collect_expense: School's account is None")
            return False

        # Debit the school's account for expense
        AccountEntry.objects.create(
            entry_ID=entry_id,
            entry_type="PL",
            user=user,
            school_account=school_account,
            amount=-expense_instance.amount,
            currency="KES",
            debit_credit_marker="Debit",
            transaction_type=expense_transaction_type,
        )

        # Update the school's balance amount
        Account.objects.filter(account_number=school_account.account_number).update(
            current_cleared_balance=F("current_cleared_balance")
            - expense_instance.amount,
            total_balance=F("total_balance") - expense_instance.amount,
        )
        return True
    except Exception as error:
        print("Error in collect_expense:", error)
        return False


from django.db.models import Sum


# def calculate_net_gains_losses():
#     # Calculate total income
#     income_total = (
#         AccountEntry.objects.filter(transaction_type__is_income=True).aggregate(
#             Sum("amount")
#         )["amount__sum"]
#         or 0
#     )

#     # Calculate total expenses
#     expense_total = (
#         AccountEntry.objects.filter(transaction_type__is_expense=True).aggregate(
#             Sum("amount")
#         )["amount__sum"]
#         or 0
#     )

#     # Calculate net gains or losses
#     net_result = income_total - expense_total

#     return net_result


def calculate_net_gains_losses(from_date=None, to_date=None):
    # Convert string dates to datetime objects
    from_date = datetime.strptime(from_date, "%Y-%m-%d") if from_date else None
    to_date = datetime.strptime(to_date, "%Y-%m-%d") if to_date else None

    # Filter entries based on the date range
    entries = AccountEntry.objects.all()
    if from_date:
        entries = entries.filter(posting_date__gte=from_date)
    if to_date:
        entries = entries.filter(posting_date__lte=to_date)

    # Calculate total income
    income_total = entries.filter(transaction_type='income').aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate total expenses
    expense_total = entries.filter(transaction_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0


    # Calculate net gains or losses
    net_result = income_total - expense_total

    return income_total, expense_total, net_result

import datetime
import random

def generate_account_number(last_serial_number=None, number_of_digits='04'):
    """
    Generates a unique account number using the current date and a serial number.

    The format of the account number is YYMMDD followed by a serial number with leading zeros.

    Args:
        last_serial_number (int, optional): The last serial number used to generate the next one. Defaults to None.
        number_of_digits (str, optional): Number of digits for the serial number. Fixed at '03'.

    Returns:
        str: The generated account number.
    """
    try:
        today_str = datetime.datetime.now().strftime('%y%m%d')

        # Initialize the serial number if not provided
        if last_serial_number is None:
            last_serial_number = 0

        # Increment and format the serial number with leading zeros
        new_serial_number = last_serial_number + 1
        serial_number_str = f"{new_serial_number:{number_of_digits}d}"

        # Combine date and serial number to form the account number
        account_number = f"{today_str}{serial_number_str}"

        return account_number
    except Exception as error:
        # Log the error message for debugging purposes
        print('generate_account_number function is raising error:', error)
        return None
from django.utils import timezone


def account_creation_finance(account_holder,short_description):
    print('account_holder',account_holder)
    # total_account = Account.objects.filter(created_at__date=datetime.datetime.today().date())
    total_account = Accounts.objects.filter( created_at__date=timezone.now().date()) 
    print('total_account',total_account.count())
    gl_line=GLLines.objects.get(name='Funds Transfer')
    print('gl_line',gl_line.pk)
    account_type=AccountTypes.objects.get(name='Equity')
    print('account_type',account_type.pk)
    account_category=AccountCategory.objects.get(name='Equity')
    print('account_category',account_category.pk)
    account_number = generate_account_number(total_account.count())
    print('account_number',account_number)
    account = Accounts.objects.create(
    account_number=account_number,
    short_description=short_description,  
    student_id_id=account_holder,
    gl_line_id=gl_line.pk,
    account_type_id=account_type.pk,
    account_category_id=account_category.pk
    )
    print('account',account)
    return account