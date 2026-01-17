import datetime
import random

from .models import *
from datetime import date
from django.utils.crypto import get_random_string
from django.db.models import Q
from django.core.exceptions import ValidationError

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


def get_current_date():
    """
    Gets the current date in YYYYMMDD format.

    Returns:
        str: The current date as a string in YYYYMMDD format.
    """
    current_date = str(date.today()).replace('-', '')
    return current_date


def generate_txn_id():
    """
    Generates a unique transaction ID in the format TXN-YYYYMMDD-RANDOM.

    Returns:
        str: The generated transaction ID.
    """
    transaction_id = "TXN-" + f"{get_current_date()}-" + str(
        int(get_random_string(length=5, allowed_chars="1234567890")))
    return transaction_id


def get_account_number(acc_holder_id=None, glline=None):
    """
    Retrieves an account object based on account holder ID or GL line ID.

    Args:
        acc_holder_id (int, optional): The account holder ID to search for.
        glline (int, optional): The GL line ID to search for.

    Returns:
        Accounts: The account object if found, otherwise None.
    """
    try:
        if acc_holder_id is not None:
            return Accounts.objects.filter(account_holder_id=acc_holder_id).first()
        if glline is not None:
            return Accounts.objects.filter(gl_line_id=glline).first()
    except Exception as error:
        # Log the error message for debugging purposes
        print("TECHNICAL ERROR WHILE GETTING ACCOUNT NO.:", error)
        return None


def get_txn_type_details(txn_id):
    """
    Retrieves transaction type details based on transaction type ID.

    Args:
        txn_id (str): The transaction type ID to search for.

    Returns:
        TransactionType: The transaction type object if found, otherwise None.
    """
    try:
        return TransactionType.objects.get(transaction_type_id=txn_id)
    except Exception as error:
        # Log the error message for debugging purposes
        print("TECHNICAL ERROR WHILE GETTING TXN TYPE DETAILS:", error)
        return None


def get_txn_code_details(txn_code):
    """
    Retrieves transaction code details based on transaction code ID.

    Args:
        txn_code (str): The transaction code ID to search for.

    Returns:
        TransactionCode: The transaction code object if found, otherwise None.
    """
    try:
        return TransactionCode.objects.get(transaction_code_id=txn_code)
    except Exception as error:
        # Log the error message for debugging purposes
        print("TECHNICAL ERROR WHILE GETTING TXN CODE DETAILS:", error)
        return None


def get_charge_code_details(charge_code):
    """
    Retrieves charge code details based on charge code ID.

    Args:
        charge_code (str): The charge code ID to search for.

    Returns:
        ChargeCode: The charge code object if found, otherwise None.
    """
    try:
        return ChargeCode.objects.get(charge_code_id=charge_code)
    except Exception as error:
        # Log the error message for debugging purposes
        print("TECHNICAL ERROR WHILE GETTING CHARGE CODE DETAILS:", error)
        return None


def common_transaction_create(transaction_id, transaction_type, from_account_id, from_currency_id, from_amount,
                              to_account_id,
                              to_currency_id, to_amount, exchange_rate_calc_mode, exchange_rate_used, charges_applied,
                              status='pending',user=None, company=None, branch=None):
    """
    Creates a new transaction record in the database.

    Args:
        transaction_id (str): Unique identifier for the transaction.
        transaction_type (str): Type of the transaction.
        from_account_id (int): ID of the account from which the amount is debited.
        from_currency_id (str): Currency code of the debited amount.
        from_amount (float): Amount debited.
        to_account_id (int): ID of the account to which the amount is credited.
        to_currency_id (str): Currency code of the credited amount.
        to_amount (float): Amount credited.
        exchange_rate_calc_mode (str): Mode of exchange rate calculation.
        exchange_rate_used (float): The exchange rate used for the transaction.
        charges_applied (float): Charges applied to the transaction.
        status (str, optional): Status of the transaction. Defaults to 'pending'.
        user (str, optional): name of the user.
        company (str, optional): name of the company.
        branch (str, optional): name of the branch.

    Returns:
        Transaction: The created transaction object if successful, otherwise None.
    """
    print('from_currency_id ', from_account_id)
    print('from_currency_id ', from_currency_id)
    print('to_account_id ', to_account_id)
    print('to_currency_id ', to_currency_id)
    try:
        obj = Transaction.objects.create(
            transaction_id=transaction_id,
            transaction_type_id=transaction_type,
            from_account_id_id=from_account_id,
            from_currency_id_id=from_currency_id,
            from_amount=from_amount,
            to_account_id_id=to_account_id,
            to_currency_id_id=to_currency_id,
            to_amount=to_amount,
            exchange_rate_calc_mode=exchange_rate_calc_mode,
            exchange_rate_used_id=exchange_rate_used,
            charges_applied=charges_applied,
            status=status,

        )
        print('its Okay')
        return obj
    except Exception as error:
        # Log the error message for debugging purposes
        print('TECHNICAL ERROR WHILE CREATING TRANSACTION:', error)
        return None


def get_cal_mode(from_currency, to_currency, base_currency='KSH'):
    """
    Determines the exchange rate calculation mode based on the currencies involved.

    Args:
        from_currency (str): Currency being debited.
        to_currency (str): Currency being credited.
        base_currency (str, optional): The base currency, defaulted to 'KSH'.

    Returns:
        str: The calculation mode ('Buy', 'Sell', 'Mid', 'No EX').
    """
    try:
        if from_currency == to_currency:
            return 'NoEx'
        elif from_currency == base_currency:
            return 'sell'
        elif to_currency == base_currency:
            return 'buy'
        else:
            return 'mid'
    except Exception as error:
        # Log the error message for debugging purposes
        print('Error determining calculation mode:', error)
        return False


def get_exchange_rate(from_currency, to_currency, base_currency='KSH'):
    """
    Retrieves the exchange rate for the specified currency pair.

    Args:
        from_currency (str): The currency from which the amount is being converted.
        to_currency (str): The currency to which the amount is being converted.
        base_currency (str): The currency to which the base currency.

    Returns:
        list: A list containing a boolean indicating success, the calculation mode, exchange rate ID,
              and the exchange rate.
    """
    try:
        print('from_currency ', from_currency, ' to_currency ', to_currency, ' base_currency ', base_currency)
        ex_rate_obj = ExchangeRate.objects.filter(
            Q(from_currency__currency_code=from_currency) & Q(to_currency__currency_code=to_currency))
        print('ex_rate_obj ', ex_rate_obj)
        if ex_rate_obj.exists():
            obj = ex_rate_obj.last()  # Get the most recent exchange rate entry
            res_cal_mode = get_cal_mode(from_currency, to_currency, base_currency)

            # Determine exchange rate based on calculation mode
            if res_cal_mode == 'NoEx':
                ex_rate_id = obj.exchange_rate_id
                ex_rate = obj.mid_rate
            elif res_cal_mode == "sell":
                ex_rate_id = obj.exchange_rate_id
                ex_rate = obj.sell_rate
            elif res_cal_mode == "buy":
                ex_rate_id = obj.exchange_rate_id
                ex_rate = obj.buy_rate
            elif res_cal_mode == "mid":
                ex_rate_id = obj.exchange_rate_id
                ex_rate = obj.mid_rate

            return [True, res_cal_mode, ex_rate_id, ex_rate]
        else:
            return [False, 'Exchange Rate Does Not Exist']

    except Exception as error:
        # Log the error message for debugging purposes
        print('get_exchange_rate raised a technical error:', error)
        return [False, str(error)]


def validate_transaction_type(txn_type_id):
    try:
        obj = TransactionType.objects.get(pk=txn_type_id)
        return obj
    except Exception as error:
        print('Error : ', error)
        return None

def get_txn_type_by_name(transaction_type_name):
    try:
        transaction_type_name = str(transaction_type_name).lower()
        obj = TransactionType.objects.filter(name__iexact=transaction_type_name)
        if obj.exists():
            return obj.first()
        else:
            return None
    except Exception as error:
        return [False, f"""{error}"""]


def create_or_get_asset_type(name, description, created_by=None):
    """
    Creates and saves an AssetType record if it doesn't exist, or retrieves the existing record.

    :param asset_type_id: Unique identifier for the asset type
    :param name: Name of the asset type
    :param description: Description of the asset type
    :param created_by: User who created the asset type (optional)
    :return: The AssetType instance
    """
    try:
        # asset_type, created = AssetType.objects.get_or_create(
        #     name=name,
        #     defaults={'description': description, 'created_by': created_by}
        # )
        asset_type = AssetType.objects.filter(name=name)
        if not asset_type.exists():
            asset_type = AssetType.objects.create(
                name = name,
                description = description,
                created_by = created_by,
            )
            return asset_type
        return asset_type.last()
    except ValidationError as e:
        print(f"Error creating or retrieving AssetType: {e}")
        return None

def create_or_get_gl_line(gl_line_number, name, description, master_gl=None, asset_type=None, created_by=None):
    """
    Creates and saves a GLLine record if it doesn't exist, or retrieves the existing record.

    :param gl_line_number: Unique number for the GL line
    :param name: Name of the GL line
    :param description: Description of the GL line
    :param master_gl: Optional master GL line (can be None)
    :param asset_type: Foreign key to AssetType (optional)
    :param created_by: User who created the GL line (optional)
    :return: The GLLine instance
    """
    try:
        gl_line, created = GLLine.objects.get_or_create(
            gl_line_number=gl_line_number,
            defaults={'name': name, 'description': description, 'master_gl': master_gl, 'asset_type': asset_type, 'created_by': created_by}
        )
        if not created:
            gl_line.name = name
            gl_line.description = description
            gl_line.master_gl = master_gl
            gl_line.asset_type = asset_type
            gl_line.created_by = created_by
            gl_line.save()
        return gl_line
    except ValidationError as e:
        print(f"Error creating or retrieving GLLine: {e}")
        return None

def create_or_get_account_type(name, description, created_by=None):
    """
    Creates and saves an AccountType record if it doesn't exist, or retrieves the existing record.

    :param name: Name of the account type
    :param description: Description of the account type
    :param created_by: User who created the account type (optional)
    :return: The AccountType instance
    """
    try:
        # account_type, created = AccountType.objects.get_or_create(
        #     name=name,
        #     defaults={'description': description, 'created_by': created_by}
        # )
        account_type = AccountType.objects.filter(name=name)
        if not account_type.exists():
            account_type = AccountType.objects.create(
                name=name,
                description = description,
                created_by = created_by,
            )
            return account_type
        else:
            return account_type.last()
    except ValidationError as e:
        print(f"Error creating or retrieving AccountType: {e}")
        return None

def create_or_get_account_category(name, description, created_by=None):
    """
    Creates and saves an AccountCategory record if it doesn't exist, or retrieves the existing record.

    :param name: Name of the account category
    :param description: Description of the account category
    :param created_by: User who created the account category (optional)
    :return: The AccountCategory instance
    """
    try:
        account_category, created = AccountCategory.objects.get_or_create(
            name=name,
            defaults={'description': description, 'created_by': created_by}
        )
        if not created:
            account_category.description = description
            account_category.created_by = created_by
            account_category.save()
        return account_category
    except ValidationError as e:
        print(f"Error creating or retrieving AccountCategory: {e}")
        return None

def create_or_get_account(account_number, account_holder=None, company=None, gl_line=None, account_type=None,
                          account_category=None, base_currency=None, overdraft_limit=0.0, opening_balance=0.0,
                          current_cleared_balance=0.0, current_uncleared_balance=0.0, total_balance=0.0, created_by=None,cr_id=None,bank_id=None, loan_id=None):
    """
    Creates and saves an Account record if it doesn't exist, or retrieves the existing record.

    :param account_number: Unique account number
    :param account_holder: Foreign key to AccountHolder (optional)
    :param company: Foreign key to Company (optional)
    :param gl_line: Foreign key to GLLine (optional)
    :param account_type: Foreign key to AccountType (optional)
    :param account_category: Foreign key to AccountCategory (optional)
    :param base_currency: Foreign key to Currency (optional)
    :param overdraft_limit: Overdraft limit for the account
    :param opening_balance: Opening balance for the account
    :param current_cleared_balance: Current cleared balance
    :param current_uncleared_balance: Current uncleared balance
    :param total_balance: Total balance
    :param created_by: User who created the account (optional)
    :return: The Account instance
    """
    try:
        account, created = Accounts.objects.get_or_create(
            account_number=account_number,
            defaults={
                'account_holder': account_holder,
                'company': company,
                'gl_line': gl_line,
                'account_type': account_type,
                'account_category': account_category,
                'base_currency': base_currency,
                'overdraft_limit': overdraft_limit,
                'opening_balance': opening_balance,
                'current_cleared_balance': current_cleared_balance,
                'current_uncleared_balance': current_uncleared_balance,
                'total_balance': total_balance,
                'created_by': created_by,
                'cr_id': cr_id,
                'loan': loan_id,
                'bank':bank_id,
            }
        )
        if not created:
            account.account_holder = account_holder
            account.company = company
            account.gl_line = gl_line
            account.account_type = account_type
            account.account_category = account_category
            account.base_currency = base_currency
            account.overdraft_limit = overdraft_limit
            account.opening_balance = opening_balance
            account.current_cleared_balance = current_cleared_balance
            account.current_uncleared_balance = current_uncleared_balance
            account.total_balance = total_balance
            account.created_by = created_by
            account.cr_id = cr_id
            account.loan = loan_id
            account.bank = bank_id
            account.save()
        return account
    except ValidationError as e:
        print(f"Error creating or retrieving Account: {e}")
        return None


def validate_mapped_custom_transaction_field(company_id, transaction_type_id):
    try:
        obj = CustomTransactionFieldMapping.objects.filter(
            Q(company_name=company_id) & Q(transaction_type_id=transaction_type_id))
        if not obj.exists():
            message = "No custom fields are mapped with the transaction type and company"
            return [False, message]

        custom_mapped_field_optional = []
        custom_mapped_field_mandatory = []
        custom_mapped_field_type_optional = []
        custom_mapped_field_type_mandatory = []
        output_list = []
        for data in obj:
            if data.is_required:
                custom_mapped_field_mandatory.append(str(data.field_name))
                custom_mapped_field_type_mandatory.append(str(data.field_type.type_name))
                my_dict = {
                    'field_name': str(data.field_name),
                    'is_required': data.is_required,
                }
                output_list.append(my_dict)
            else:
                custom_mapped_field_optional.append(str(data.field_name))
                custom_mapped_field_type_optional.append(str(data.field_type.type_name))
                my_dict = {
                    'field_name': str(data.field_name),
                    'is_required': data.is_required,
                }
                output_list.append(my_dict)

        return [True, custom_mapped_field_optional, custom_mapped_field_mandatory, custom_mapped_field_type_optional,
                custom_mapped_field_type_mandatory,output_list]

    except Exception as error:

        print('Error ', error)
        return [False,f'''{error}''']

def check_field_validation_value(company_id, transaction_type_id,field_name, field_value):
    """
    field_name : type is list
    field_value : type is list
    """
    output_list = []
    for field_name, field_value in zip(field_name, field_value):
        obj = CustomTransactionFieldMapping.objects.filter(
            Q(company_name=company_id) & Q(transaction_type_id=transaction_type_id) & Q(field_name__field_name=field_name))
        if not obj.exists():
            my_dict = {
                'field_name': field_name,
                'field_value': field_value,
                'is_required': None,
                'Message' : 'Invalid Field'
            }
            output_list.append(my_dict)
        else:
            obj_last = obj.last()
            if obj_last.is_required:
                if field_value == '' or field_value.strip() == '' or field_value is None:
                    my_dict = {
                        'field_name': field_name,
                        'field_value': field_value,
                        'is_required': obj_last.is_required,
                        'Message': 'This is a mandatory field. Please enter a valid value'
                    }
                    output_list.append(my_dict)
    return output_list
