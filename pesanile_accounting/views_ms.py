from .scripts import *
from django.contrib.auth import authenticate, login
from .scripts_pr import apply_payment_to_payable, apply_payment_to_receivable, get_receivable_and_payable_details
from .account_entries import *
def common_message(status_code, message=None):
    message = {
        'status_code': status_code,
        'status': 'Success' if status_code != 0 else 'Failed',
        'message': message
    }
    return message

def transaction_type_ms(pk, debit_currency,debit_account,credit_currency,credit_account):
    obj = TransactionType.objects.get(pk=pk)
    obj.debit_currency = None if len(debit_currency) == 0 else debit_currency
    obj.debit_account = None if len(debit_account) == 0 else debit_account
    obj.credit_currency = None if len(credit_currency) == 0 else credit_currency
    obj.credit_account = None if len(credit_account) == 0 else credit_account
    obj.save()  # Save normally form
    form.save_m2m()  # save many to many fields
    """
    Need to check it
    """



def account_receivable_create_ms(pk, payment_term_period,payment_term_milestone,payment_term_amount):
    obj = AccountReceivable.objects.get(pk=pk)
    obj.payment_term_period = None if len(payment_term_period) == 0 else payment_term_period
    obj.payment_term_milestone = None if len(payment_term_milestone) == 0 else payment_term_milestone
    obj.payment_term_amount = None if len(payment_term_amount) == 0 else payment_term_amount
    obj.save()
    """
    Need to check it
    """


def receivable_and_payable_transaction_ms(transaction_type,receivable,payable,amount, request_user_obj):
    request_user_obj = authenticate(email='admin@bharathbrands.in', password='1234')
    print('request_user_obj ',request_user_obj)
    get_txn_obj = validate_transaction_type(transaction_type)
    print('get_txn_obj ',get_txn_obj)
    if get_txn_obj is None:
        return common_message(status_code=1, message="Invalid Transaction Type")
    # form.save()
    transaction_type_id = get_txn_obj.pk
    amount = eval(amount)
    if receivable == 'None' and payable == 'None':
        return common_message(status_code=1, message="Receivable and payable should not be empty")
    if str(get_txn_obj.name).lower() == 'payment' and payable == 'None':
        return common_message(status_code=1, message="kindly select the payable")
    if str(get_txn_obj.name).lower() == 'receipt' and receivable == 'None':
        return common_message(status_code=1, message="kindly select the receivable")
    # here logic for payable
    if str(get_txn_obj.name).lower() == 'payment':
        payable = apply_payment_to_payable(payable, amount)
        if not payable[0]:
            return common_message(status_code=1, message=f"""{payable[1]}""")
    # here logic for payable
    if str(get_txn_obj.name).lower() == 'receipt':
        payable = apply_payment_to_receivable(receivable, amount)
        if not payable[0]:
            return common_message(status_code=1, message=f"""{payable[1]}""")
    # Accounting Process
    print('Im okay till here..')
    account_category = get_txn_obj.category_of_account.account_category_id
    dr_obj = Accounts.objects.filter(account_category_id=account_category)
    if not dr_obj.exists():
        return common_message(status_code=1, message="Company account Not Found")
    dr_obj_last = dr_obj.last()
    dr_acc = dr_obj_last.pk
    cr_acc = 16  # Just fixed credit acc id
    if str(get_txn_obj.name).lower() == 'receipt':
        cr_acc, dr_acc = dr_acc, cr_acc
    # company_id = 'COMP--5524'
    logged_user_details = request_user_obj.company_name
    company_id = logged_user_details.company_name
    local_currency_name = logged_user_details.local_currency
    local_currency_id = logged_user_details.local_currency.pk
    teller_profile = TellerProfile.objects.get(user=request_user_obj)
    transaction_type = get_txn_obj.name
    is_teller = teller_profile.can_process_transaction(float(amount), str(transaction_type).lower())
    if not is_teller[0]:
        return common_message(status_code=1, message=is_teller[1])
    get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                    base_currency=str(local_currency_name))
    if not get_ex_rate[0]:
        return common_message(status_code=1, message=get_ex_rate[1])
    res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
    txn_type_obj = TransactionType.objects.get(name=transaction_type)
    dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
    cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
    credit_amount = float(amount) * float(ex_rate)
    entry_type = 'PL'
    transaction_id = generate_txn_id()
    obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id, amount,
                                    cr_acc,
                                    local_currency_id, amount, res_cal_mode, ex_rate_id,
                                    charges_applied=False,
                                    status='pending')
    resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                         credit_currency=local_currency_id,
                         total_debit_amt=float(amount), debit_currency=local_currency_id,
                         dr_acc=dr_acc,
                         cr_acc=cr_acc,
                         debit_credit_marker='DebitCredit', user=request_user_obj.pk)
    # form_obj = form.save(commit=False)
    obj.transaction_id = transaction_id
    obj.exchange_rate_calc_mode = res_cal_mode
    obj.exchange_rate_used_id = ex_rate_id
    obj.to_amount = amount
    obj.status = 'success' if resp else 'pending'
    obj.save()
    # update the teller
    is_cleared = teller_profile.clear_teller_amount(float(amount), str(transaction_type))
    return common_message(status_code=0, message='Success')


def post_receivable_and_payable_transaction_ms(transaction_type,reference_number,receivable,payable,amount,request_user_obj):
    
    get_txn_obj = validate_transaction_type(transaction_type)
    print('get_txn_obj',get_txn_obj)
    if get_txn_obj is None:
        return common_message(status_code=1, message="Invalid Transaction Type")
    # form.save()
    transaction_type_id = get_txn_obj.pk
    amount = eval(amount)
    print('amount',amount,str(get_txn_obj.name).lower())
    # here logic for payable
    if str(get_txn_obj.name).lower() == 'payment':
        payable = apply_payment_to_payable(reference_number, amount)
        if not payable[0]:
            return common_message(status_code=1, message=f"""{payable[1]}""")
    # here logic for payable
    if str(get_txn_obj.name).lower() == 'receipt':
        payable = apply_payment_to_receivable(reference_number, amount)
        if not payable[0]:
            return common_message(status_code=1, message=f"""{payable[1]}""")
    account_category = get_txn_obj.category_of_account.account_category_id
    print('account_category',account_category)
    dr_obj = Accounts.objects.filter(account_category_id=account_category)
    print('dr_obj',dr_obj)
    if not dr_obj.exists():
        return common_message(status_code=1, message=f"""Company account Not Found""")
    dr_obj_last = dr_obj.last()
    dr_acc = dr_obj_last.pk
    cr_acc = 16  # Just fixed credit acc id
    if str(get_txn_obj.name).lower() == 'receipt':
        cr_acc, dr_acc = dr_acc, cr_acc
    company_id = 'COMP--5524'
    logged_user_details = request_user_obj
    company_id = company_id
    local_currency_name = 'Kenya Shilling'
    local_currency_id = '254-3182'
    # # teller_profile = TellerProfile.objects.get(user=request_user_obj)
    # # transaction_type = get_txn_obj.name
    # # is_teller = teller_profile.can_process_transaction(float(amount), str(transaction_type).lower())
    # # if not is_teller[0]:
    # #     return common_message(status_code=1, message=is_teller[1])
    # get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
    #                                 base_currency=str(local_currency_name))
    # if not get_ex_rate[0]:
    #     return common_message(status_code=1, message=get_ex_rate[1])
    # res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
    # txn_type_obj = TransactionType.objects.get(pk=transaction_type)
    # print('txn_type_obj',txn_type_obj)
    # dr_txn_code = txn_type_obj.debit_transaction_code
    # cr_txn_code = txn_type_obj.credit_transaction_code
    # credit_amount = float(amount) * float(ex_rate)
    # entry_type = 'PL'
    # transaction_id = generate_txn_id()
    # obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id, amount,
    #                                 cr_acc,
    #                                 local_currency_id, amount, res_cal_mode, ex_rate_id,
    #                                 charges_applied=False,
    #                                 status='pending')
    # resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
    #                      credit_currency=local_currency_id,
    #                      total_debit_amt=float(amount), debit_currency=local_currency_id,
    #                      dr_acc=dr_acc,
    #                      cr_acc=cr_acc,
    #                      debit_credit_marker='DebitCredit', user=request_user_obj, company=company_id,
    #                      ref_no=reference_number)
    if str(get_txn_obj.name).lower() =='fees collection':            
            type1=TransactionType.objects.get(name=get_txn_obj.name)
            print('type',type1.pk)
            debit=TransactionType.objects.get(transaction_type_id=type1.pk)
            debit_account_str = debit.debit_account.strip("[]'")  # Remove brackets and quotes
            debit_account_int = int(debit_account_str)
            print('debit', debit_account_int)
            credit_account_str = debit.credit_account.strip("[]'")  # Remove brackets and quotes
            credit_account_int = int(credit_account_str)
            print('debit', credit_account_int)
            accounts = Accounts.objects.filter(account_id=debit_account_int)
            print('Dr_Acc:', accounts)

            cr_accounts = Accounts.objects.filter(account_id=credit_account_int)
            print('cr:', cr_accounts)
            accounts=accounts.first()
            cr_accounts=cr_accounts.first()
            # accounts = Accounts.objects.filter(account_id__in=debit_account_ids)
            # cr_accounts = Accounts.objects.filter(account_id__in=credit_account_ids)
            Dr_Acc=Accounts.objects.get(short_description=accounts)
            print('Dr_Acc',Dr_Acc)

            Cr_Acc=Accounts.objects.get(short_description=cr_accounts)
            print('Cr_Acc',Cr_Acc)

            entry_type='PL'
            transaction_id = generate_txn_id()
            txn_type_obj = TransactionType.objects.get(transaction_type_id=transaction_type)
            dr_txn_code = txn_type_obj.debit_transaction_code
            cr_txn_code = txn_type_obj.credit_transaction_code
            local_currency_id = 'shelling-8837'
            local_currency_name = 'KSH'
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                    base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                return common_message(status_code=1, message=get_ex_rate[1])
            res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
            txn_type_obj = TransactionType.objects.get(pk=transaction_type)
            print('txn_type_obj',txn_type_obj)
            dr_txn_code = txn_type_obj.debit_transaction_code
            cr_txn_code = txn_type_obj.credit_transaction_code
            credit_amount = float(amount) * float(ex_rate)
            entry_type = 'PL'
            transaction_id = generate_txn_id()
            obj = common_transaction_create(transaction_id, transaction_type_id, Dr_Acc.pk, local_currency_id, amount,
                                    Cr_Acc.pk,
                                    local_currency_id, amount, res_cal_mode, ex_rate_id,
                                    charges_applied=False,
                                    status='pending')
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                         credit_currency=local_currency_id,
                         total_debit_amt=float(amount), debit_currency=local_currency_id,
                         dr_acc=Dr_Acc.pk,
                         cr_acc=Cr_Acc.pk,
                         debit_credit_marker='DebitCredit', user=request_user_obj, company=company_id,
                         ref_no=reference_number)
            print("created the entry")
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                    base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                print("why")
    if str(get_txn_obj).lower() =='salary payment':            
            type1=TransactionType.objects.get(name=get_txn_obj)
            print('type',type1.debit_account)
            # cr_account=type1.credit_account[0]
            # print('account',cr_account)
            debit=TransactionType.objects.get(transaction_type_id=type1.pk)
            debit_account_str = debit.debit_account.strip("[]'")  # Remove brackets and quotes
            debit_account_int = int(debit_account_str)
            print('debit', debit_account_int)
            credit_account_str = debit.credit_account.strip("[]'")  # Remove brackets and quotes
            credit_account_int = int(credit_account_str)
            print('debit', credit_account_int)
            accounts = Accounts.objects.filter(account_id=debit_account_int)
            print('Dr_Acc:', accounts)

            cr_accounts = Accounts.objects.filter(account_id=credit_account_int)
            print('cr:', cr_accounts)
            accounts=accounts.first()
            cr_accounts=cr_accounts.first()
            Dr_Acc=Accounts.objects.get(short_description=accounts)
            Cr_Acc=Accounts.objects.get(short_description=cr_accounts)
            print('Dr_Acc',Dr_Acc)
            # Dr_Acc.current_cleared_balance-=amount
            # Dr_Acc.total_balance-=amount
            # Dr_Acc.save()
            entry_type='PL'
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                        base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                return common_message(status_code=1, message=get_ex_rate[1])
            res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
            txn_type_obj = TransactionType.objects.get(pk=transaction_type)
            print('txn_type_obj',txn_type_obj)
            transaction_id = generate_txn_id()
            txn_type_obj = TransactionType.objects.get(transaction_type_id=transaction_type)
            dr_txn_code = txn_type_obj.debit_transaction_code
            cr_txn_code = txn_type_obj.credit_transaction_code
            local_currency_id = 'shelling-8837'
            local_currency_name = 'KSH'

            obj = common_transaction_create(transaction_id, transaction_type_id, Dr_Acc.pk, local_currency_id, amount,
                                    Cr_Acc.pk,
                                    local_currency_id, amount, res_cal_mode, ex_rate_id,
                                    charges_applied=False,
                                    status='pending')
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                         credit_currency=local_currency_id,
                         total_debit_amt=float(amount), debit_currency=local_currency_id,
                         dr_acc=Dr_Acc.pk,
                         cr_acc=Cr_Acc.pk,
                         debit_credit_marker='DebitCredit', user=request_user_obj, company=company_id,
                         ref_no=reference_number)
            print("created the entry")
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                    base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                print("why")


    # form_obj = form.save(commit=False)
    # obj.transaction_id = transaction_id
    # obj.exchange_rate_calc_mode = res_cal_mode
    # obj.exchange_rate_used_id = ex_rate_id
    # obj.to_amount = amount
    # obj.status = 'success' if resp else 'pending'
    # obj.save()
    
    # update the teller
    # is_cleared = teller_profile.clear_teller_amount(float(amount), str(transaction_type))
    return common_message(status_code=0, message='Success')


def account_payment_create_ms(reference_number,amount,request_user_obj):
    get_txn_obj = get_txn_type_by_name('payment')
    if get_txn_obj is None:
        return common_message(status_code=1, message="Invalid Transaction Type")
    # form.save()
    transaction_type_id = get_txn_obj.pk
    amount = eval(amount)
    account_category = get_txn_obj.category_of_account.account_category_id
    dr_obj = Accounts.objects.filter(account_category_id=account_category)
    if not dr_obj.exists():
        return common_message(status_code=1, message="Company account Not Found")
    dr_obj_last = dr_obj.last()
    dr_acc = dr_obj_last.pk
    cr_acc = 16  # Just fixed credit acc id
    if str(get_txn_obj.name).lower() == 'receipt':
        cr_acc, dr_acc = dr_acc, cr_acc
    company_id = 'COMP--5524'
    logged_user_details = request_user_obj.company_name
    company_id = logged_user_details.company_name
    local_currency_name = logged_user_details.local_currency
    local_currency_id = logged_user_details.local_currency.pk
    teller_profile = TellerProfile.objects.get(user=request_user_obj)
    transaction_type = get_txn_obj.name
    is_teller = teller_profile.can_process_transaction(float(amount), str(transaction_type).lower())
    if not is_teller[0]:
        return common_message(status_code=1, message=is_teller[1])
    get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                    base_currency=str(local_currency_name))
    if not get_ex_rate[0]:
        return common_message(status_code=1, message=get_ex_rate[1])
    res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
    txn_type_obj = TransactionType.objects.get(name=transaction_type)
    dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
    cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
    credit_amount = float(amount) * float(ex_rate)
    entry_type = 'PL'
    transaction_id = generate_txn_id()
    obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id, amount,
                                    cr_acc,
                                    local_currency_id, amount, res_cal_mode, ex_rate_id,
                                    charges_applied=False,
                                    status='pending')
    resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                         credit_currency=local_currency_id,
                         total_debit_amt=float(amount), debit_currency=local_currency_id,
                         dr_acc=dr_acc,
                         cr_acc=cr_acc,
                         debit_credit_marker='DebitCredit', user=request_user_obj.pk)
    # form_obj = form.save(commit=False)
    obj.transaction_id = transaction_id
    obj.exchange_rate_calc_mode = res_cal_mode
    obj.exchange_rate_used_id = ex_rate_id
    obj.to_amount = amount
    obj.status = 'success' if resp else 'pending'
    obj.save()
    form_obj = form.save(commit=False)
    form_obj.transaction_id = transaction_id
    form_obj.save()
    # update the teller
    is_cleared = teller_profile.clear_teller_amount(float(amount), str(transaction_type))
    return common_message(status_code=0, message='Success')



def account_receipt_create_ms(reference_number,amount,request_user_obj):
    get_txn_obj = get_txn_type_by_name('receipt')
    if get_txn_obj is None:
        return common_message(status_code=1, message='Invalid Transaction Type')
    # form.save()
    transaction_type_id = get_txn_obj.pk
    amount = eval(amount)
    account_category = get_txn_obj.category_of_account.account_category_id
    dr_obj = Accounts.objects.filter(account_category_id=account_category)
    if not dr_obj.exists():
        return common_message(status_code=1, message='Company account Not Found')
    dr_obj_last = dr_obj.last()
    dr_acc = dr_obj_last.pk
    cr_acc = 16  # Just fixed credit acc id
    if str(get_txn_obj.name).lower() == 'receipt':
        cr_acc, dr_acc = dr_acc, cr_acc
    company_id = 'COMP--5524'
    logged_user_details = request_user_obj.company_name
    company_id = logged_user_details.company_name
    local_currency_name = logged_user_details.local_currency
    local_currency_id = logged_user_details.local_currency.pk
    teller_profile = TellerProfile.objects.get(user=request_user_obj)
    transaction_type = get_txn_obj.name
    is_teller = teller_profile.can_process_transaction(float(amount), str(transaction_type).lower())
    if not is_teller[0]:
        return common_message(status_code=1, message=is_teller[1])
    get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                    base_currency=str(local_currency_name))
    if not get_ex_rate[0]:
        return common_message(status_code=1, message=get_ex_rate[1])
    res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
    txn_type_obj = TransactionType.objects.get(name=transaction_type)
    dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
    cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
    credit_amount = float(amount) * float(ex_rate)
    entry_type = 'PL'
    transaction_id = generate_txn_id()
    obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id, amount,
                                    cr_acc,
                                    local_currency_id, amount, res_cal_mode, ex_rate_id,
                                    charges_applied=False,
                                    status='pending')
    resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                         credit_currency=local_currency_id,
                         total_debit_amt=float(amount), debit_currency=local_currency_id,
                         dr_acc=dr_acc,
                         cr_acc=cr_acc,
                         debit_credit_marker='DebitCredit', user=request_user_obj.pk)
    # form_obj = form.save(commit=False)
    obj.transaction_id = transaction_id
    obj.exchange_rate_calc_mode = res_cal_mode
    obj.exchange_rate_used_id = ex_rate_id
    obj.to_amount = amount
    obj.status = 'success' if resp else 'pending'
    obj.save()
    form_obj = form.save(commit=False)
    form_obj.transaction_id = transaction_id
    form_obj.save()
    # update the teller
    is_cleared = teller_profile.clear_teller_amount(float(amount), str(transaction_type))
    return common_message(status_code=0, message='Success')


def custom_transaction_field_mapping_create_ms(company,transaction_type,
                                                   field_name, field_type, is_required):
    try:
        if len(field_name) != len(is_required):
            is_required.insert(0, False)
        identification_key = generate_custom_id(pre_fix='IDK')
        for field_name, field_type, is_required in zip(field_name, field_type, is_required, ):
            obj = CustomTransactionFieldMapping.objects.create(
                company_id=company,
                transaction_type_id=transaction_type,
                field_name_id=field_name,
                field_type_id=field_type,
                is_required=True if is_required == 'on' else False,
                identification_key=identification_key,
                created_by_id=request_user_obj.pk,
            )
        return common_message(status_code=0, message='Success')
    except Exception as error:
        return common_message(status_code=1, message=f'''{error}''')

def get_acc_by_currency_and_txn_type_id_ms(currency_id, txn_type_id,currency_source):
    try:
        # Get the transaction type object
        transaction_type = get_object_or_404(TransactionType, pk=txn_type_id)
        print('transaction_type ', transaction_type)

        # Filter accounts based on the currency and transaction type
        if currency_source == 'from':
            from_currency_list = transaction_type.debit_currency
            from_account_list = transaction_type.debit_account
            for cur_id, acc_id in zip(eval(from_currency_list), eval(from_account_list)):
                if cur_id == currency_id:
                    accounts = Accounts.objects.filter(pk=acc_id)
                    account_data = [{'id': account.pk, 'name': account.account_number} for account in accounts]
                    return JsonResponse({'accounts': account_data})
            accounts = []
        elif currency_source == 'to':
            to_currency_list = transaction_type.credit_currency
            to_account_list = transaction_type.credit_account
            for cur_id, acc_id in zip(eval(to_currency_list), eval(to_account_list)):
                if cur_id == currency_id:
                    accounts = Accounts.objects.filter(pk=acc_id)
                    account_data = [{'id': account.pk, 'name': account.account_number} for account in accounts]

                    return JsonResponse({'accounts': account_data})
            accounts = []
        else:
            accounts = []

        # Prepare the list of account IDs and names (or other required data)
        account_data = [{'id': account.pk, 'name': account.account_number} for account in accounts]

        return JsonResponse({'accounts': account_data})

    except Exception as error:
        print('error ', error)
        return common_message(status_code=0, message=f'''{error}''')

def service_payment_create_ms():
    user = form.data.get('user')
    account_holder = form.data.get('debit_acc_number')
    credit_acc_number_holder_id = form.data.get('credit_acc_number')
    transaction_type = form.data.get('transaction_type')
    amount = total_amount = from_amount = to_amount = form.data.get('amount')
    get_acc_holder_number_obj = get_account_number(
        acc_holder_id=account_holder)
    get_acc_holder_number_obj_cr = get_account_number(
        acc_holder_id=credit_acc_number_holder_id)
    if get_acc_holder_number_obj is None or get_acc_holder_number_obj_cr is None:
        return common_message(status_code=1, message='Account not found')
    from_account_id = get_acc_holder_number_obj.account_id
    from_currency_name = get_acc_holder_number_obj.base_currency
    from_currency_id = get_acc_holder_number_obj.base_currency.currency_id
    to_account_id = get_acc_holder_number_obj_cr.account_id
    to_currency_name = get_acc_holder_number_obj_cr.base_currency
    to_currency_id = get_acc_holder_number_obj_cr.base_currency.currency_id
    # get txn type details transaction_code_id
    get_txn_obj = get_txn_type_details(transaction_type)
    if get_txn_obj is None:
        return common_message(status_code=1, message='Transaction Type Not Founds')

    debit_transaction_code = get_txn_obj.debit_transaction_code.transaction_code_id
    credit_transaction_code = get_txn_obj.credit_transaction_code.transaction_code_id
    charge_code = get_txn_obj.charge_code.charge_code_id

    # =========== GET TRANSACTION CODE DETAILS ===============
    get_dr_txn_code_obj = get_txn_code_details(debit_transaction_code)
    get_cr_txn_code_obj = get_txn_code_details(credit_transaction_code)
    if get_dr_txn_code_obj is None or get_cr_txn_code_obj is None:
        return common_message(status_code=1, message='Transaction Code Not Not Found')
    # ============= debit txn code details ======================
    get_dr_debit_gl_line = get_dr_txn_code_obj.debit_gl_line.gl_line_id
    get_dr_credit_gl_line = get_dr_txn_code_obj.credit_gl_line.gl_line_id
    get_dr_overdraft_check = get_dr_txn_code_obj.overdraft_check
    # ============= credit txn code details ======================
    get_cr_debit_gl_line = get_cr_txn_code_obj.debit_gl_line.gl_line_id
    get_cr_credit_gl_line = get_cr_txn_code_obj.credit_gl_line.gl_line_id
    get_cr_overdraft_check = get_cr_txn_code_obj.overdraft_check
    # ============ CHARGE CODE DETAILS ===========================
    get_charge_code = get_charge_code_details(charge_code)
    if get_charge_code is None:
        return common_message(status_code=1, message='Charge Code Not Found')
    charge_amount = get_charge_code.charge_amount
    currency = get_charge_code.currency
    gl_line_to_credit = get_charge_code.gl_line_to_credit.gl_line_id
    get_gl_acc_no = get_account_number(glline=gl_line_to_credit)
    gl_acc_no = get_gl_acc_no.account_id
    transaction_code_to_use = get_charge_code.transaction_code_to_use.transaction_code_id

    # ======================== Entries =============================
    transaction_id = generate_txn_id()

    details_payload = {
        'get_acc_holder_number': get_acc_holder_number_obj.account_id,
        'amount': amount,
        'get_dr_debit_gl_line': get_dr_debit_gl_line,
        'get_dr_credit_gl_line': get_dr_credit_gl_line,
        'get_dr_overdraft_check': get_dr_overdraft_check,
        'get_cr_debit_gl_line': get_cr_debit_gl_line,
        'get_cr_credit_gl_line': get_cr_credit_gl_line,
        'get_cr_overdraft_check': get_cr_overdraft_check,
        'charge_amount': charge_amount,
        'currency': currency,
        'gl_line_to_credit': gl_line_to_credit,
        'transaction_code_to_use': transaction_code_to_use,
        'transaction_id': transaction_id,
    }
    resp = get_exchange_rate(from_currency_name, to_currency_name)
    if not resp[0]:
        return common_message(status_code=1, message=str(resp[1]))
    exchange_rate_calc_mode = resp[1]
    exchange_rate_used = resp[2]
    ex_rate = resp[3]
    print('amount ', amount)
    print('exchange_rate_calc_mode ', exchange_rate_calc_mode)
    print('exchange_rate_used ', exchange_rate_used)
    print('ex_rate ', ex_rate)
    print('total amount in ksh ', float(amount) * float(ex_rate))
    to_amount = float(amount) * float(ex_rate)
    # ================== CREATE TRANSACTION ==================
    txn_resp_or_obj = transaction_create(transaction_id, transaction_type, from_account_id,
                                         from_currency_id, from_amount, to_account_id, to_currency_id,
                                         to_amount, exchange_rate_calc_mode, exchange_rate_used,
                                         charges_applied=False, status='pending')
    if txn_resp_or_obj is None:
        return common_message(status_code=1, message="TECHNICAL ERROR WHILE CREATING TXN")
    # ============================== Account Entries ==========================
    entry_type = 'AL'
    amount = float(amount) - float(charge_amount)
    get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code,
                              credit_transaction_code, amount, total_debit_amt=total_amount,
                              currency=from_currency_id,
                              dr_acc=from_account_id, cr_acc=to_account_id,
                              debit_credit_marker='DebitCredit', user=None)
    get_resp2 = account_entry(entry_type, transaction_id, transaction_code_to_use,
                              transaction_code_to_use, charge_amount,
                              currency=to_currency_id,
                              dr_acc=None, cr_acc=gl_acc_no,
                              debit_credit_marker='Credit', user=None)

    # now debit transaction code and credit txn code wise wise entries
    # ========================= DR. TXN CODE =========================
    get_dr_gl_acc_no_obj = get_account_number(glline=get_dr_debit_gl_line)
    dr_gl_acc_no = get_dr_gl_acc_no_obj.account_id
    get_cr_gl_acc_no_obj = get_account_number(glline=get_dr_credit_gl_line)
    cr_gl_acc_no = get_cr_gl_acc_no_obj.account_id
    get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code,
                              credit_transaction_code, total_amount, total_debit_amt=total_amount,
                              currency=from_currency_id,
                              dr_acc=dr_gl_acc_no, cr_acc=cr_gl_acc_no,
                              debit_credit_marker='DebitCredit', user=None)
    print('DR TXN code ', get_resp1)
    # ========================= CR. TXN CODE =========================
    get_cr_dr_gl_acc_no_obj = get_account_number(glline=get_cr_debit_gl_line)
    cr_dr_gl_acc_no = get_cr_dr_gl_acc_no_obj.account_id
    get_cr_gl_acc_no_obj = get_account_number(glline=get_cr_credit_gl_line)
    cr_gl_acc_no = get_cr_gl_acc_no_obj.account_id
    get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code,
                              credit_transaction_code, total_amount, total_debit_amt=total_amount,
                              currency=from_currency_id,
                              dr_acc=cr_dr_gl_acc_no, cr_acc=cr_gl_acc_no,
                              debit_credit_marker='DebitCredit', user=None)
    print('CR TXN code ', get_resp1)
    # update the txn update that txn happened successfully
    txn_resp_or_obj.status = 'success'
    txn_resp_or_obj.save()
    return common_message(status_code=0, message=f"Transaction Done Done {transaction_id}")


def transaction_create_ms(request_user_obj, local_currency,transaction_type,from_account_id,from_currency_id,
                          fc_id,tc_id,from_amount=None,to_amount=None,to_account_id=None,to_currency_id=None,charges_applied=None):
    logged_user_details = request_user_obj.company_name
    teller_profile = TellerProfile.objects.get(user=request_user_obj)
    if not from_amount:
        from_amount = to_amount

    is_teller = teller_profile.can_process_transaction(float(from_amount), str(transaction_type))
    if not is_teller[0]:
        return common_message(status_code=1, message=is_teller[1])
    get_ex_rate = get_exchange_rate(str(from_currency_id), str(to_currency_id),
                                    base_currency=str(local_currency))
    if not get_ex_rate[0]:
        return common_message(status_code=1, message=get_ex_rate[1])
    print('get_ex_rate ', get_ex_rate)
    res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
    txn_type_obj = TransactionType.objects.get(name=transaction_type)
    dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
    cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
    credit_amount = float(from_amount) * float(ex_rate)
    entry_type = 'PL'
    transaction_id = generate_txn_id()
    resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount,
                         credit_currency=tc_id,
                         total_debit_amt=float(from_amount), debit_currency=fc_id,
                         dr_acc=from_account_id,
                         cr_acc=to_account_id,
                         debit_credit_marker='DebitCredit', user=request_user_obj.pk)
    print('resp ', resp)
    form_obj = form.save(commit=False)
    form_obj.transaction_id = transaction_id
    form_obj.exchange_rate_calc_mode = res_cal_mode
    form_obj.exchange_rate_used_id = ex_rate_id
    form_obj.to_amount = credit_amount
    form_obj.status = 'success' if resp else 'pending'
    form_obj.save()
    # update the teller
    is_cleared = teller_profile.clear_teller_amount(float(from_amount), str(transaction_type))
    print('is_cleared ', is_cleared)
    return common_message(status_code=0, message='Success')

def special_transaction_create_ms(transaction_type,from_account_id,from_currency_id,
                                  fc_id,tc_id,from_amount,to_account_id,to_currency_id,charges_applied,request_user_obj):
    logged_user_details = request_user_obj.company_name
    print('logged_user_details ', logged_user_details)
    local_currency = logged_user_details.local_currency
    teller_profile = TellerProfile.objects.get(user=request_user_obj)
    print('teller_profile ', teller_profile)
    is_teller = teller_profile.can_process_transaction(float(from_amount), str(transaction_type))
    if not is_teller[0]:
        return common_message(status_code=0, message=is_teller[1])
    get_ex_rate = get_exchange_rate(str(from_currency_id), str(to_currency_id),
                                    base_currency=str(local_currency))
    if not get_ex_rate[0]:
        return common_message(status_code=0, message=get_ex_rate[1])
    res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
    txn_type_obj = TransactionType.objects.get(name=transaction_type)
    dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
    cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
    credit_amount = float(from_amount) * float(ex_rate)
    entry_type = 'PL'
    transaction_id = generate_txn_id()
    resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount,
                         credit_currency=tc_id,
                         total_debit_amt=float(from_amount), debit_currency=fc_id,
                         dr_acc=from_account_id,
                         cr_acc=to_account_id,
                         debit_credit_marker='DebitCredit', user=request_user_obj.pk)
    print('resp ', resp)
    form_obj = form.save(commit=False)
    form_obj.transaction_id = transaction_id
    form_obj.exchange_rate_calc_mode = res_cal_mode
    form_obj.exchange_rate_used_id = ex_rate_id
    form_obj.to_amount = credit_amount
    form_obj.status = 'success' if resp else 'pending'
    form_obj.save()
    # update the teller
    is_cleared = teller_profile.clear_teller_amount(float(from_amount), str(transaction_type))
    print('is_cleared ', is_cleared)
    return common_message(status_code=0, message='Success')
