from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from .forms import *
from .scripts import *
from .account_entries import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .scripts_pr import *
from django.http import HttpResponseRedirect
import datetime
import random
from sub_part.models import *
from datetime import date
from django.utils.crypto import get_random_string
from .tenant_ways import tenant_create_save,pre_setup_tenant_create_save
from .check_permission import check_user_role_return_db
def exclude_field(field_name):
    return field_name not in ['created_at', 'updated_at', 'created_by','updated_by']


def check_transaction_type(request):
    transaction_type_id = request.GET.get('transaction_type_id')
    is_special = False
    print('hre.....')

    if transaction_type_id:
        try:
            transaction_type = TransactionType.objects.get(pk=transaction_type_id)
            debit_currency = transaction_type.debit_currency
            if debit_currency:
                is_special = 'PreDefineAccount'
            if str(transaction_type.name).lower() == 'payment' or str(transaction_type.name).lower() == 'receipt':
                is_special = "PaymentAndReceipt"

        except TransactionType.DoesNotExist:
            print('ThanksHere')
            pass
    print('here..')
    print('is_special ', is_special)
    return JsonResponse({'is_special': is_special})


def get_acc_by_currency_and_txn_type_id(request, currency_id, txn_type_id):
    currency_source = request.GET.get('currency_source', 'from')  # Default to 'from' if not provided
    print('currency_source ', currency_source)

    # Get the transaction type object
    transaction_type = get_object_or_404(TransactionType, pk=txn_type_id)
    print('transaction_type ', transaction_type)

    # Filter accounts based on the currency and transaction type
    if currency_source == 'from':
        from_currency_list = transaction_type.debit_currency
        from_account_list = transaction_type.debit_account
        print('from_currency_list ', from_currency_list)
        print('from_account_list ', from_account_list)
        for cur_id, acc_id in zip(eval(from_currency_list), eval(from_account_list)):
            print('cur_id ', cur_id)
            print('acc_id ', acc_id)
            if cur_id == currency_id:
                accounts = Accounts.objects.filter(pk=acc_id)
                account_data = [{'id': account.pk, 'name': account.account_number} for account in accounts]
                return JsonResponse({'accounts': account_data})
        accounts = []
    elif currency_source == 'to':
        to_currency_list = transaction_type.credit_currency
        to_account_list = transaction_type.credit_account
        print('to_currency_list ', to_currency_list)
        print('to_account_list ', to_account_list)
        for cur_id, acc_id in zip(eval(to_currency_list), eval(to_account_list)):
            if cur_id == currency_id:
                accounts = Accounts.objects.filter(pk=acc_id)
                account_data = [{'id': account.pk, 'name': account.account_number} for account in accounts]

                return JsonResponse({'accounts': account_data})
        accounts = []
    else:
        accounts = []

    # Prepare the list of account IDs and names (or other required data)
    print(' im here....')
    print('accounts ', accounts)
    account_data = [{'id': account.pk, 'name': account.account_number} for account in accounts]

    return JsonResponse({'accounts': account_data})


# View to check if the transaction type is special
# def check_transaction_type(request, transaction_type_id):
#     try:
#         print('transaction_type_id ', transaction_type_id)
#         transaction_type = TransactionType.objects.get(pk=transaction_type_id)
#         is_special = transaction_type.debit_currency  # Assuming you have a boolean field `is_special`
#         # is_special = True
#
#         if is_special:
#             # Return special transaction details
#             from_currency = transaction_type.debit_currency  # Assuming you have these fields
#             to_currency = transaction_type.credit_currency
#             response = {
#                 'is_special': True,
#
#                 # 'from_currency_id': from_currency.id if from_currency else None,
#                 # 'to_currency_id': to_currency.id if to_currency else None,
#                 'from_currency_id': from_currency,
#                 'to_currency_id': to_currency,
#             }
#             print('response ', response)
#
#             return JsonResponse(response)
#         else:
#             return JsonResponse({'is_special': False})
#     except TransactionType.DoesNotExist:
#         return JsonResponse({'is_special': False})


# View to get account by currency
def get_account_by_currency(request, currency_id):
    try:
        account = Accounts.objects.filter(currency_id=currency_id).first()
        return JsonResponse({'account_id': account.id if account else None})
    except Accounts.DoesNotExist:
        return JsonResponse({'account_id': None})


def get_account_currency(request, account_id):
    print('account ', account_id)
    account = Accounts.objects.get(pk=account_id)
    print('account ', account)
    return JsonResponse({'currency_id': account.base_currency.pk})


@login_required(login_url='user_login')
def dashboard_finance(request):

    # app_name, model_name = 'pesanile_accounting','Company'
    # no_of_company = check_user_role_return_db('pesanile_accounting','Company', request, list_all=False).count()
    # no_of_user = check_user_role_return_db('pesanile_accounting','User', request, list_all=False).count()
    no_of_user=Transaction.objects.all().count()
    no_of_currency=Currency.objects.all().count()
    no_of_glline=GLLine.objects.all().count()
    no_of_account_type=AccountType.objects.all().count()
    no_of_accounts=Accounts.objects.all().count()
    no_of_account_entries=AccountEntry.objects.all().count()
    no_of_transaction_type=TransactionType.objects.all().count()
    no_of_receivable=AccountReceivable.objects.all().count()
    no_of_payable=AccountPayable.objects.all().count()
    # no_of_currency = check_user_role_return_db('pesanile_accounting','Currency', request, list_all=True).count()
    # no_of_glline = check_user_role_return_db('pesanile_accounting','GLLine', request, list_all=True).count()
    # no_of_account_type = check_user_role_return_db('pesanile_accounting','AccountType', request, list_all=True).count()
    # no_of_accounts = check_user_role_return_db('pesanile_accounting','Accounts', request, list_all=False).count()
    # no_of_account_entries = check_user_role_return_db('pesanile_accounting','AccountEntry', request, list_all=False).count()
    # no_of_custom_type = check_user_role_return_db('pesanile_accounting','CustomFieldType', request, list_all=True).count()
    # no_of_custom_field = check_user_role_return_db('pesanile_accounting','CustomField', request, list_all=True).count()
    # no_of_transaction_type = check_user_role_return_db('pesanile_accounting','TransactionType', request, list_all=False).count()
    # no_of_payable = check_user_role_return_db('pesanile_accounting','AccountPayable', request, list_all=False).count()
    # no_of_receivable = check_user_role_return_db('pesanile_accounting','AccountReceivable', request, list_all=False).count()
    # no_of_payable = AccountPayable.objects.all().count()
    # no_of_receivable = AccountReceivable.objects.all().count()
    context = {
        'screen_name': 'Dashboard',
        # 'no_of_company': no_of_company,
          'no_of_user':no_of_user,
          'no_of_currency':no_of_currency,'no_of_glline':no_of_glline,
        'no_of_account_type': no_of_account_type, 'no_of_accounts':no_of_accounts,
         'no_of_transaction_type':no_of_transaction_type,
        # 'no_of_custom_field':no_of_custom_field, 'no_of_custom_type':no_of_custom_type,
        'no_of_account_entries':no_of_account_entries,
         'no_of_payable':no_of_payable,
        'no_of_receivable':no_of_receivable,
    }
    template_name = 'dashboard_finance.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def service_payment(request):
    if request.method == 'POST':
        form = ServicePaymentForm(request.POST)
        if form.is_valid():
            # Handle form processing here (e.g., sending emails, saving data)
            #messages.success(request, 'Form submitted successfully!')
            return redirect(reverse('admin:service_payment_form'))
    else:
        form = ServicePaymentForm()
        return render(request, 'admin/service_payment_form.html', {'form': form})

@login_required(login_url='user_login')
def service_payment_create(request):
    screen_name = 'Service Payment'
    if request.method == 'POST':
        form = ServicePaymentForms(request.POST)
        if form.is_valid():
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
                context = {'form': form, 'create_url': reverse('service_payment_create'),
                           'list_url': reverse('service_payment_list'), "message": "Account not founds"
                           }
                template_name = 'pesanile_accounting/create_everything.html'
                return render(request, template_name, context)
            print('get_acc_holder_number_obj ', get_acc_holder_number_obj)
            from_account_id = get_acc_holder_number_obj.account_id
            from_currency_name = get_acc_holder_number_obj.base_currency
            from_currency_id = get_acc_holder_number_obj.base_currency.currency_id
            to_account_id = get_acc_holder_number_obj_cr.account_id
            to_currency_name = get_acc_holder_number_obj_cr.base_currency
            to_currency_id = get_acc_holder_number_obj_cr.base_currency.currency_id
            # get txn type details transaction_code_id
            get_txn_obj = get_txn_type_details(transaction_type)
            if get_txn_obj is None:
                context = {
                    'form': form, 'create_url': reverse('service_payment_create'),
                    'list_url': reverse('service_payment_list'), "message": "Transaction Type Not Founds"
                }
                template_name = 'pesanile_accounting/create_everything.html'
                return render(request, template_name, context)

            debit_transaction_code = get_txn_obj.debit_transaction_code.transaction_code_id
            credit_transaction_code = get_txn_obj.credit_transaction_code.transaction_code_id
            charge_code = get_txn_obj.charge_code.charge_code_id

            # =========== GET TRANSACTION CODE DETAILS ===============
            get_dr_txn_code_obj = get_txn_code_details(debit_transaction_code)
            get_cr_txn_code_obj = get_txn_code_details(credit_transaction_code)
            if get_dr_txn_code_obj is None or get_cr_txn_code_obj is None:
                context = {
                    'form': form, 'create_url': reverse('service_payment_create'),
                    'list_url': reverse('service_payment_list'), "message": "Transaction Code Not Not Found"
                }
                template_name = 'pesanile_accounting/create_everything.html'
                return render(request, template_name, context)
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
                context = {
                    'form': form,
                    'create_url': reverse('service_payment_create'),
                    'list_url': reverse('service_payment_list'),
                    "message": "Charge Code Not Found"
                }
                template_name = 'pesanile_accounting/create_everything.html'
                return render(request, template_name, context)
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
                context = {
                    'form': form,
                    'create_url': reverse('service_payment_create'),
                    'list_url': reverse('service_payment_list'),
                    "message": str(resp[1])
                }
                template_name = 'pesanile_accounting/create_everything.html'
                return render(request, template_name, context)
            print('resp ', resp)
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
                context = {
                    'form': form,
                    'create_url': reverse('service_payment_create'),
                    'list_url': reverse('service_payment_list'),
                    "message": "TECHNICAL ERROR WHILE CREATING TXN"
                }
                template_name = 'pesanile_accounting/create_everything.html'
                return render(request, template_name, context)
            # ============================== Account Entries ==========================
            entry_type = 'AL'
            amount = float(amount) - float(charge_amount)
            get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code,
                                      credit_transaction_code, amount, total_debit_amt=total_amount,
                                      currency=from_currency_id,
                                      dr_acc=from_account_id, cr_acc=to_account_id,
                                      debit_credit_marker='DebitCredit', user=request.user.pk,
                                      company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                      )
            get_resp2 = account_entry(entry_type, transaction_id, transaction_code_to_use,
                                      transaction_code_to_use, charge_amount,
                                      currency=to_currency_id,
                                      dr_acc=None, cr_acc=gl_acc_no,
                                      debit_credit_marker='Credit', user=request.user.pk,
                                      company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                      )

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
                                      debit_credit_marker='DebitCredit', user=request.user.pk,
                                      company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                      )
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
                                      debit_credit_marker='DebitCredit', user=request.user.pk,
                                      company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                      )
            print('CR TXN code ', get_resp1)
            # update the txn update that txn happened successfully
            txn_resp_or_obj.status = 'success'
            txn_resp_or_obj.save()
            context = {
                'form': form,
                'create_url': reverse('service_payment_create'),
                'list_url': reverse('service_payment_list'),
                "message": f"Transaction Done Done {transaction_id}"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)
            # logic
        else:
            context = {
                'form': form.errors,
                'create_url': reverse('service_payment_create'),
                'list_url': reverse('service_payment_list'),
                'screen_name': screen_name
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)
    if request.method == 'GET':
        form = ServicePaymentForms()
        context = {
            'form': form,
            'create_url': reverse('service_payment_create'),
            'list_url': reverse('service_payment_list'),
            'screen_name': screen_name
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def service_payment_list(request):
    screen_name = "Service Payment"
    is_action_required = False
    app_name, model_name = 'pesanile_accounting','ServicePayment'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'create_url': reverse('service_payment_create'),
        'list_url': reverse('service_payment_list'),
        'is_action_required': is_action_required,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)

@login_required(login_url='user_login')
def transaction_create(request):
    screen_name = 'Transaction'
    if request.method == 'POST':
        form = TransactionForm(request.POST,created_by=request.user)
        if form.is_valid():
            logged_user_details = request.user.company
            local_currency = logged_user_details.local_currency
            transaction_type = str(form.cleaned_data.get('transaction_type'))
            from_account_id = str(request.POST.get('from_account_id'))
            from_currency_id = str(form.cleaned_data.get('from_currency_id'))
            # =============== Same ====================
            fc_id = request.POST.get('from_currency_id')
            tc_id = request.POST.get('to_currency_id')
            from_amount = request.POST.get('from_amount', None)
            to_amount = request.POST.get('to_amount', None)
            to_account_id = request.POST.get('to_account_id')
            to_currency_id = form.cleaned_data.get('to_currency_id')
            charges_applied = request.POST.get('charges_applied')
            # teller_profile = TellerProfile.objects.get(user=request.user)
            print('from_amount ',from_amount)
            print('to_amount ',to_amount)
            if not from_amount:
                from_amount = to_amount
            print('from amount ', from_amount)


            # is_teller = teller_profile.can_process_transaction(float(from_amount), str(transaction_type))
            # if not is_teller[0]:
            #     context = {
            #         'form': form,
            #         'screen_name': screen_name,
            #         'create_url': reverse('transaction_create'),
            #         'list_url': reverse('transaction_list'),
            #         "message": is_teller[1]
            #     }
            #     template_name = 'pesanile_accounting/transaction_create.html'
            #     return render(request, template_name, context)
            get_ex_rate = get_exchange_rate(str(from_currency_id), str(to_currency_id),
                                            base_currency=str(local_currency))
            if not get_ex_rate[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": get_ex_rate[1]
                }
                template_name = 'pesanile_accounting/transaction_create.html'
                return render(request, template_name, context)
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
                                 debit_credit_marker='DebitCredit', user=request.user.pk,
                                 company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                 )
            print('resp ', resp)
            form_obj = form.save(commit=False)
            form_obj.transaction_id = transaction_id
            form_obj.exchange_rate_calc_mode = res_cal_mode
            form_obj.exchange_rate_used_id = ex_rate_id
            form_obj.to_amount = credit_amount
            form_obj.status = 'success' if resp else 'pending'
            # =========== Tenant Save Start =================
            # form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user) # Tenant Save
            # =========== Tenant Save End =================
            # form_obj.save()
            #messages.success(request, 'Success')
            # update the teller
            # is_cleared = teller_profile.clear_teller_amount(float(from_amount), str(transaction_type))
            # print('is_cleared ', is_cleared)
            return redirect('transaction_list')
        else:
            print('forms.error ',form.errors)
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('transaction_create'),
                'list_url': reverse('transaction_list'),
                "message": "PROVIDE VALID DETAILS",
                "is_form_error": True
            }
            template_name = 'pesanile_accounting/transaction_create.html'
            
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TransactionForm(created_by=request.user)
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_create'),
            'list_url': reverse('transaction_list'),
        }
        template_name = 'pesanile_accounting/transaction_create.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def special_transaction_create(request, special_txn):
    screen_name = 'Transaction'
    if request.method == 'POST':
        print('special form....')
        print(request.POST)
        form = SpecialTransactionForm(request.POST)
        if form.is_valid():
            print('request user ', request.user)
            logged_user_details = request.user.company_name
            print('logged_user_details ', logged_user_details)
            local_currency = logged_user_details.local_currency
            transaction_type = str(form.cleaned_data.get('transaction_type'))
            from_account_id = str(request.POST.get('from_account_id'))
            from_currency_id = str(form.cleaned_data.get('from_currency_id'))
            # =============== Same ====================
            fc_id = request.POST.get('from_currency_id')
            tc_id = request.POST.get('to_currency_id')
            from_amount = request.POST.get('from_amount')
            to_account_id = request.POST.get('to_account_id')
            to_currency_id = form.cleaned_data.get('to_currency_id')
            charges_applied = request.POST.get('charges_applied')
            print('from_account_id', from_account_id)
            print('from_currency_id', from_currency_id)
            print('to_account_id', to_account_id)
            print('to_currency_id', to_currency_id)
            print('transaction_type ', transaction_type)
            # teller_profile = TellerProfile.objects.get(user=request.user)
            # print('teller_profile ', teller_profile)
            # is_teller = teller_profile.can_process_transaction(float(from_amount), str(transaction_type))
            # if not is_teller[0]:
            #     context = {
            #         'form': form,
            #         'screen_name': screen_name,
            #         'create_url': reverse('transaction_create'),
            #         'list_url': reverse('transaction_list'),
            #         "message": is_teller[1]
            #     }
            #     template_name = 'pesanile_accounting/special_transaction_create.html'
            #     return render(request, template_name, context)
            get_ex_rate = get_exchange_rate(str(from_currency_id), str(to_currency_id),
                                            base_currency=str(local_currency))
            if not get_ex_rate[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": get_ex_rate[1]
                }
                template_name = 'pesanile_accounting/special_transaction_create.html'
                return render(request, template_name, context)
            print('get_ex_rate ', get_ex_rate)
            res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
            txn_type_obj = TransactionType.objects.get(name=transaction_type)
            dr_txn_code = txn_type_obj.debit_transaction_code
            cr_txn_code = txn_type_obj.credit_transaction_code
            credit_amount = float(from_amount) * float(ex_rate)
            entry_type = 'PL'
            transaction_id = generate_txn_id()
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount,
                                 credit_currency=tc_id,
                                 total_debit_amt=float(from_amount), debit_currency=fc_id,
                                 dr_acc=from_account_id,
                                 cr_acc=to_account_id,
                                 debit_credit_marker='DebitCredit', user=request.user.pk,
                                 company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                 )
            print('resp ', resp)
            form_obj = form.save(commit=False)
            form_obj.transaction_id = transaction_id
            form_obj.exchange_rate_calc_mode = res_cal_mode
            form_obj.exchange_rate_used_id = ex_rate_id
            form_obj.to_amount = credit_amount
            form_obj.status = 'success' if resp else 'pending'
            # =========== Tenant Save Start =================
            # form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            # update the teller
            # is_cleared = teller_profile.clear_teller_amount(float(from_amount), str(transaction_type))
            # print('is_cleared ', is_cleared)
            return redirect('transaction_list')
        else:
            print('form error ', form.errors)
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('transaction_create'),
                'list_url': reverse('transaction_list'),
                "message": "PROVIDE VALID DETAILS",
                "is_form_error": True
            }
            template_name = 'pesanile_accounting/transaction_create.html'
            
            return render(request, template_name, context)

    if request.method == 'GET':
        try:
            txn_obj = TransactionType.objects.get(pk=special_txn)
            form = SpecialTransactionForm(initial={
                'transaction_type': txn_obj.pk
            })
            context = {
                'form': form,
                'txn_obj': txn_obj,
                'screen_name': screen_name,
                'create_url': reverse('transaction_create'),
                'list_url': reverse('transaction_list'),
            }
            template_name = 'pesanile_accounting/special_transaction_create.html'
            return render(request, template_name, context)
        except Exception as error:
            print('error ', error)
            return redirect('transaction_create')


@login_required(login_url='user_login')
def transaction_list(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name,branch_id)

    screen_name = "Transaction"
    is_action_required = False
    app_name, model_name = 'pesanile_accounting','Transaction'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    print('obj ',obj)
    obj_fields = [field for field in Transaction._meta.get_fields() if exclude_field(field.name)]
    print('obj ',obj_fields)
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('transaction_create'),
        'list_url': reverse('transaction_list'),
        'is_action_required': is_action_required,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)

import datetime

@login_required(login_url='user_login')
def account_create(request):
    screen_name = 'Accounts'
    if request.method == 'POST':
        print('Im here.....')
        form = AccountForm(request.POST,created_by=request.user)
        if form.is_valid():
            # =========== Tenant Save Start =================
            branch_name=form.cleaned_data['branch_name']
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_list')
        else:
            print(form.errors)
            context = {
                'form': form,
                'create_url': reverse('account_create'),
                'list_url': reverse('account_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        print('datetime.datetime.today().date() ',datetime.datetime.today().date())
        total_account = Accounts.objects.filter(created_at__date=datetime.datetime.today().date())
        print('account_number ',total_account.count())
        account_number = generate_account_number(total_account.count())
        print('account_number ',account_number)
        print('request.user ',request.user)
        form = AccountForm(initial={'account_number':'ACC-'+str(account_number)})
        # branch_obj = Branch.objects.filter(created_by_id=request.user.pk)
        # print('branch_obj ',branch_obj)
        
        context = {
            'form': form,
            'screen_name': screen_name,
            # 'branch_obj':branch_obj,
            'create_url': reverse('account_create'),
            'list_url': reverse('account_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_list(request):
    screen_name = "Accounts"
    is_action_required = False
    app_name, model_name = 'pesanile_accounting','Accounts'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    obj_fields = [field for field in Accounts._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_create'),
        'list_url': reverse('account_list'),
        'update_url': 'account-update',
        'delete_url': 'account-delete',
        'is_action_required': is_action_required,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


# =========== below here ================
@login_required(login_url='user_login')
def account_restriction_create(request):
    screen_name = 'Account Restriction'
    if request.method == 'POST':
        form = AccountRestrictionForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_restriction_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('account_restriction_create'),
                'list_url': reverse('account_restriction_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountRestrictionForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_restriction_create'),
            'list_url': reverse('account_restriction_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_restriction_list(request):
    screen_name = "Account Restrictions"
    is_action_required = True
    app_name, model_name = 'pesanile_accounting','AccountRestriction'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    obj_fields = [field for field in AccountRestriction._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_restriction_create'),
        'list_url': reverse('account_restriction_list'),
        'update_url': 'account-restriction-update',
        'delete_url': 'account-restriction-delete',
        'is_action_required': is_action_required,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def overdraft_limit_create(request):
    screen_name = 'Overdraft Limit'
    if request.method == 'POST':
        form = OverdraftLimitForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('overdraft_limit_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('overdraft_limit_create'),
                'list_url': reverse('overdraft_limit_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = OverdraftLimitForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('overdraft_limit_create'),
            'list_url': reverse('overdraft_limit_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def overdraft_limit_list(request):
    screen_name = "Overdraft Limit"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','OverdraftLimit'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in OverdraftLimit._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('overdraft_limit_create'),
        'list_url': reverse('overdraft_limit_list'),
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def glline_create(request):
    screen_name = 'GLLine'
    if request.method == 'POST':
        form = GLLineForm(request.POST)
        if form.is_valid():
            # =========== Pre Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            resp = pre_setup_tenant_create_save(form_obj, request.user)  # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('glline_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('glline_create'),
                'list_url': reverse('glline_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = GLLineForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('glline_create'),
            'list_url': reverse('glline_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def glline_list(request):
    screen_name = "GL Line"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','GLLine'
    obj = check_user_role_return_db(app_name, model_name, request,list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in GLLine._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('glline_create'),
        'list_url': reverse('glline_list'),
        'update_url': 'glline-update',
        'delete_url': 'glline-delete',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def asset_type_category_create(request):
    screen_name = 'Asset Type Category'
    if request.method == 'POST':
        form = AssetTypeCategoryForm(request.POST)
        if form.is_valid():
            # =========== Pre Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            form_obj.save()
            resp = pre_setup_tenant_create_save(form_obj, request.user)  # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('asset_type_category_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('asset_type_category_create'),
                'list_url': reverse('asset_type_category_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AssetTypeCategoryForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('asset_type_category_create'),
            'list_url': reverse('asset_type_category_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def asset_type_category_list(request):
    screen_name = "Asset Type Category"
    allow_update = True
    allow_delete = True
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AssetTypeCategory'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in AssetTypeCategory._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'allow_update': allow_update,
        'allow_delete': allow_delete,
        'create_url': reverse('asset_type_category_create'),
        'list_url': reverse('asset_type_category_list'),
        'update_url': reverse('asset_type_category_update'),
        'delete_url': reverse('asset_type_category_delete'),
    }

    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def asset_type_category_update(request,pk):
    screen_name = 'Asset Type Category'
    if request.method == 'POST':
        form = AssetTypeCategoryForm(request.POST)
        if form.is_valid():
            # =========== Pre Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            resp = pre_setup_tenant_create_save(form_obj, request.user)  # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('asset_type_category_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('asset_type_category_create'),
                'list_url': reverse('asset_type_category_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AssetTypeCategoryForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('asset_type_category_create'),
            'list_url': reverse('asset_type_category_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def asset_type_category_delete(request,pk):
    try:
        obj = AssetTypeCategory.objects.get(pk=pk)
        obj.delete()
        return redirect('asset_type_category_list')
    except Exception as error:
        print('Error ', error)
        return redirect('asset_type_category_list')


@login_required(login_url='user_login')
def asset_type_create(request):
    screen_name = 'Asset Type'
    if request.method == 'POST':
        form = AssetTypeForm(request.POST)
        if form.is_valid():
            # =========== Pre Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            resp = pre_setup_tenant_create_save(form_obj, request.user)  # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('asset_type_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('asset_type_create'),
                'list_url': reverse('asset_type_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AssetTypeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('asset_type_create'),
            'list_url': reverse('asset_type_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def asset_type_list(request):
    screen_name = "Asset Type"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AssetType'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in AssetType._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('asset_type_create'),
        'list_url': reverse('asset_type_list'),
        'update_url': 'asset-type-update',
        'delete_url': 'asset-type-delete',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def account_holder_create(request):
    screen_name = 'Account Holder'
    if request.method == 'POST':
        form = AccountHolderForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_holder_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('account_holder_create'),
                'list_url': reverse('account_holder_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountHolderForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_holder_create'),
            'list_url': reverse('account_holder_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_holder_list(request):
    screen_name = "Account Holder"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountHolder'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in AccountHolder._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_holder_create'),
        'list_url': reverse('account_holder_list'),
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def account_category_create(request):
    screen_name = 'Account Category'
    if request.method == 'POST':
        form = AccountCategoryForm(request.POST)
        if form.is_valid():
            print('data',form.cleaned_data)
            print('user',request.user)
            # =========== Pre Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            form_obj.save()
            # form_obj.save()
            resp = pre_setup_tenant_create_save(form_obj, request.user)  # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_category_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('account_category_create'),
                'list_url': reverse('account_category_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountCategoryForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_category_create'),
            'list_url': reverse('account_category_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_category_list(request):
    screen_name = "Account Category"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountCategory'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in AccountCategory._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_category_create'),
        'list_url': reverse('account_category_list'),
        'update_url': 'account-category-update',
        'delete_url': 'account-category-delete',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def account_type_category_create(request):
    screen_name = 'Account Type Category'
    if request.method == 'POST':
        form = AccountTypeCategoryForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            form_obj.created_by=request.user
            form_obj.updated_by=request.user
            form_obj.save()
            print('data',form_obj)

            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_type_category_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('account_type_category_create'),
                'list_url': reverse('account_type_category_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountTypeCategoryForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_type_category_create'),
            'list_url': reverse('account_type_category_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_type_category_list(request):
    screen_name = "Account Type Category"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountTypeCategory'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in AccountTypeCategory._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_type_category_create'),
        'list_url': reverse('account_type_category_list'),
        'update_url': 'account-type-category-update',
        'delete_url': 'account-type-category-delete',
        'is_action_required': True,
    }

    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def account_type_create(request):
    screen_name = 'Account Type'
    if request.method == 'POST':
        form = AccountTypeForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = pre_setup_tenant_create_save(form_obj, request.user) # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_type_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('account_type_create'),
                'list_url': reverse('account_type_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountTypeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_type_create'),
            'list_url': reverse('account_type_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_type_list(request):
    screen_name = "Account Type"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountType'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in AccountType._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_type_create'),
        'list_url': reverse('account_type_list'),
        'update_url': 'account-type-update',
        'delete_url': 'account-type-delete',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def exchange_rate_create(request):
    screen_name = 'Exchange Rate'
    if request.method == 'POST':
        form = ExchangeRateForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('exchange_rate_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('exchange_rate_create'),
                'list_url': reverse('exchange_rate_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = ExchangeRateForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('exchange_rate_create'),
            'list_url': reverse('exchange_rate_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def exchange_rate_list(request):
    screen_name = "Exchange Rate"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','ExchangeRate'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in ExchangeRate._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('exchange_rate_create'),
        'list_url': reverse('exchange_rate_list'),
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def currency_create(request):
    screen_name = 'Currency'
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('currency_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('currency_create'),
                'list_url': reverse('currency_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CurrencyForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('currency_create'),
            'list_url': reverse('currency_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def currency_list(request):
    screen_name = "Currency"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','Currency'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in Currency._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('currency_create'),
        'list_url': reverse('currency_list'),
        'update_url': 'currency-update',
        'delete_url': 'currency-delete',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def company_create(request):
    screen_name = 'Company'
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by=request.user
            obj.save()
            #messages.success(request, 'Success')
            return redirect('company_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('company_create'),
                'list_url': reverse('company_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CompanyForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('company_create'),
            'list_url': reverse('company_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def company_update(request,pk):
    screen_name = 'Company Update'
    obj = Company.objects.get(pk=pk)
    if request.method == 'POST':
        form = CompanyForm(request.POST, instance=obj)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by=request.user
            obj.save()
            #messages.success(request, 'Success')
            return redirect('company_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('company_create'),
                'list_url': reverse('company_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CompanyForm(instance=obj)
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('company_create'),
            'list_url': reverse('company_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def company_list(request):
    screen_name = "Company"
    app_name, model_name = 'pesanile_accounting','Company'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    print('obj ',obj)
    obj_fields = [field for field in Company._meta.get_fields() if
                  field.name not in ['created_at', 'updated_at','website','address','created_by','number_of_branches','number_of_staffs','end_of_month_date']]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'is_company': True,
        'obj_fields': obj_fields,
        'create_url': reverse('company_create'),
        'list_url': reverse('company_list'),
        'update_url': 'company-update',
        'delete_url': 'company-delete',
        'add_new':'no',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)

# ==========================Branch ============================

@login_required(login_url='user_login')
def branch_create(request):
    screen_name = 'Branch'
    if request.method == 'POST':
        form = BranchForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            form_obj.company_name = request.user.company_name
            form_obj.created_by = request.user
            form_obj.updated_by = request.user
            form_obj.save()
            # resp = tenant_create_save(form_obj,request.user, request.user.company_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('branch_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('branch_create'),
                'list_url': reverse('branch_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = BranchForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('branch_create'),
            'list_url': reverse('branch_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def branch_list(request):
    screen_name = "Branch"
    app_name, model_name = 'pesanile_accounting','Branch'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    obj_fields = [field for field in Branch._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('branch_create'),
        'list_url': reverse('branch_list'),
        'update_url': 'branch-update',
        'delete_url': 'branch-delete',
        'add_new':'yes',
        'is_action_required': True,
    }

    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


# ==========================BANK ACCOUNT============================


@login_required(login_url='user_login')
def bankacc_create(request):
    screen_name = 'Bank Account'
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('bankacc_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('bankacc_create'),
                'list_url': reverse('bankacc_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/bankacc_create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CompanyForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('bankacc_create'),
            'list_url': reverse('bankacc_list'),
        }
        template_name = 'pesanile_accounting/bankacc_create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def bankacc_list(request):
    screen_name = "Company"
    obj = Company.objects.all()
    obj_fields = Company._meta.get_fields()
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('bankacc_create'),
        'list_url': reverse('bankacc_list'),
    }
    
    template_name = 'pesanile_accounting/bankacc_list_everything.html'
    return render(request, template_name, context)

# ====================== above done ==================

@login_required(login_url='user_login')
def transaction_code_create(request):
    screen_name = 'Transaction Code'
    if request.method == 'POST':
        form = TransactionCodeForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('transaction_code_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('transaction_code_create'),
                'list_url': reverse('transaction_code_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TransactionCodeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_code_create'),
            'list_url': reverse('transaction_code_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_code_list(request):
    screen_name = "Transaction Code"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','TransactionCode'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in TransactionCode._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('transaction_code_create'),
        'list_url': reverse('transaction_code_list'),
        'update_url': 'transaction-code-update',
        'delete_url': 'transaction-code-delete',
        'add_new':'yes',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def charge_code_classification_create(request):
    screen_name = 'Charge Code Classfication'
    if request.method == 'POST':
        form = ChargeCodeClassificationForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            form_obj.save() # enable because of using tenant save
            resp = tenant_create_save(form_obj, request.user)  # Tenant Save
            # =========== Tenant Save End =================
            # messages.success(request, 'Success')
            return redirect('charge_code_classification_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('charge_code_classification_create'),
                'list_url': reverse('charge_code_classification_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = ChargeCodeClassificationForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('charge_code_classification_create'),
            'list_url': reverse('charge_code_classification_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def charge_code_classification_list(request):
    screen_name = "Charge Code Classification"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting', 'ChargeCodeClassification'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in ChargeCodeClassification._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('charge_code_classification_create'),
        'list_url': reverse('charge_code_classification_list'),
    }

    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def charge_code_create(request):
    screen_name = 'Charge Code'
    if request.method == 'POST':
        form = ChargeCodeForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('charge_code_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('charge_code_create'),
                'list_url': reverse('charge_code_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = ChargeCodeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('charge_code_create'),
            'list_url': reverse('charge_code_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def charge_code_list(request):
    screen_name = "Charge Code"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','ChargeCode'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in ChargeCode._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('charge_code_create'),
        'list_url': reverse('charge_code_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def interest_code_create(request):
    screen_name = 'Interest Code'
    if request.method == 'POST':
        form = InterestCodeForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('interest_code_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('interest_code_create'),
                'list_url': reverse('interest_code_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = InterestCodeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('interest_code_create'),
            'list_url': reverse('interest_code_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def interest_code_list(request):
    screen_name = "Interest Code"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','InterestCode'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in InterestCode._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('interest_code_create'),
        'list_url': reverse('interest_code_list'),
        'add_new':'yes',
        'is_action_required': False,
    }

    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)

@login_required(login_url='user_login')
def transaction_type_create(request):
    screen_name = 'Transaction Type'
    if request.method == 'POST':
        form = TransactionTypeForm(request.POST)
        print('REQUEST POST ', request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            debit_currency = request.POST.getlist('debit_currency')
            debit_account = request.POST.getlist('debit_account')
            credit_currency = request.POST.getlist('credit_currency')
            credit_account = request.POST.getlist('credit_account')
            form_obj.debit_currency = None if len(debit_currency) == 0 else debit_currency
            form_obj.debit_account = None if len(debit_account) == 0 else debit_account
            form_obj.credit_currency = None if len(credit_currency) == 0 else credit_currency
            form_obj.credit_account = None if len(credit_account) == 0 else credit_account
            # form_obj.company_name = request.user.company_name
            form_obj.created_by = request.user
            form_obj.updated_by = request.user
            form_obj.save()
            form.save_m2m()  # save many to many fields
            #messages.success(request, 'Success')
            return redirect('transaction_type_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('transaction_type_create'),
                'list_url': reverse('transaction_type_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/transaction_type_create.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        obj_account = Accounts.objects.all()
        obj_currency = Currency.objects.all()
        form = TransactionTypeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_type_create'),
            'list_url': reverse('transaction_type_list'),
            'obj_account': obj_account,
            'obj_currency': obj_currency,
        }
        template_name = 'pesanile_accounting/transaction_type_create.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_type_list(request):
    screen_name = "Transaction Type"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','TransactionType'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in TransactionType._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('transaction_type_create'),
        'list_url': reverse('transaction_type_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_details_create(request):
    screen_name = 'Transaction Detail'
    if request.method == 'POST':
        form = TransactionDetailForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('transaction_details_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('transaction_details_create'),
                'list_url': reverse('transaction_details_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TransactionDetailForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_details_create'),
            'list_url': reverse('transaction_details_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_details_list(request):
    screen_name = "Transaction Detail"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','TransactionDetail'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in TransactionDetail._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('transaction_details_create'),
        'list_url': reverse('transaction_details_list'),
        'add_new':'no',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def account_entry_create(request):
    screen_name = 'Account Entry'
    if request.method == 'POST':
        form = AccountEntryForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_entry_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('account_entry_create'),
                'list_url': reverse('account_entry_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountEntryForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_entry_create'),
            'list_url': reverse('account_entry_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_entry_list(request):
    screen_name = "Account Entry"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountEntry'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in AccountEntry._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_entry_create'),
        'list_url': reverse('account_entry_list'),
        'add_new':'no',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def teller_profile_create(request):
    screen_name = 'Teller Profile'
    if request.method == 'POST':
        form = TellerProfileForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            form_obj.save()
            resp = tenant_create_save(form_obj,request.user) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('teller_profile_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('teller_profile_create'),
                'list_url': reverse('teller_profile_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TellerProfileForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('teller_profile_create'),
            'list_url': reverse('teller_profile_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def teller_profile_list(request):
    screen_name = "Teller Profile"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','TellerProfile'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in TellerProfile._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('teller_profile_create'),
        'list_url': reverse('teller_profile_list'),
        'add_new':'yes',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)

# ===================== Account Payable & Receivable, and payment and receipt =================
@login_required(login_url='user_login')
def account_receivable_create(request):
    screen_name = 'Account Receivable'
    if request.method == 'POST':
        form = AccountReceivableForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            payment_term_period = request.POST.getlist('payment_term_period')
            payment_term_milestone = request.POST.getlist('payment_term_milestone')
            payment_term_amount = request.POST.getlist('payment_term_amount')
            form_obj.payment_term_period = None if len(payment_term_period) == 0 else payment_term_period
            form_obj.payment_term_milestone = None if len(payment_term_milestone) == 0 else payment_term_milestone
            form_obj.payment_term_amount = None if len(payment_term_amount) == 0 else payment_term_amount
            # =========== Tenant Save Start =================
            # form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_receivable_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('account_receivable_create'),
                'list_url': reverse('account_receivable_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/account_receivable_create.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountReceivableForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_receivable_create'),
            'list_url': reverse('account_receivable_list'),
        }
        template_name = 'pesanile_accounting/account_receivable_create.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_receivable_list(request):
    screen_name = 'Account Receivable'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountReceivable'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    # obj_fields = AccountReceivable._meta.get_fields()
    context = {
        'obj': obj,
        'screen_name': screen_name,
        # 'obj_fields': obj_fields,
        'create_url': reverse('account_receivable_create'),
        'list_url': reverse('account_receivable_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/account_receivable_list.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def account_payable_create(request):
    screen_name = 'Account Payable'
    if request.method == 'POST':
        form = AccountPayableForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            payment_term_period = request.POST.getlist('payment_term_period')
            payment_term_milestone = request.POST.getlist('payment_term_milestone')
            payment_term_amount = request.POST.getlist('payment_term_amount')
            form_obj.payment_term_period = None if len(payment_term_period) == 0 else payment_term_period
            form_obj.payment_term_milestone = None if len(payment_term_milestone) == 0 else payment_term_milestone
            form_obj.payment_term_amount = None if len(payment_term_amount) == 0 else payment_term_amount
            # =========== Tenant Save Start =================
            # form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('account_payable_list')
        else:
            print('form error ', form.errors)
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('account_payable_create'),
                'list_url': reverse('account_payable_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/account_payable_create.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountPayableForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('account_payable_create'),
            'list_url': reverse('account_payable_list'),
        }
        template_name = 'pesanile_accounting/account_payable_create.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_payable_list(request):
    screen_name = 'Account Payable'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountPayable'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    # obj_fields = AccountPayable._meta.get_fields()
    context = {
        'obj': obj,
        'screen_name': screen_name,
        # 'obj_fields': obj_fields,
        'create_url': reverse('account_payable_create'),
        'list_url': reverse('account_payable_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/account_payable_list.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def payment_create(request):
    screen_name = 'Payment'
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('payment_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('payment_create'),
                'list_url': reverse('payment_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = PaymentForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('payment_create'),
            'list_url': reverse('payment_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def payment_list(request):
    screen_name = 'Payment'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','Payment'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = Payment._meta.get_fields()
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('payment_create'),
        'list_url': reverse('payment_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def receipt_create(request):
    screen_name = 'Receipt'
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('receipt_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('receipt_create'),
                'list_url': reverse('receipt_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = ReceiptForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('receipt_create'),
            'list_url': reverse('receipt_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def receipt_list(request):
    screen_name = "Receipt"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','Receipt'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = Receipt._meta.get_fields()
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('receipt_create'),
        'list_url': reverse('receipt_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_type_classification_create(request):
    screen_name = 'Transaction Type Classification'
    if request.method == 'POST':
        form = TransactionTypeClassificationForm(request.POST)
        if form.is_valid():
            print('form.is_valid()',form.is_valid())
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            form_obj.save()
            resp = tenant_create_save(form_obj,request.user) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('transaction_type_classification_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('transaction_type_classification_create'),
                'list_url': reverse('transaction_type_classification_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TransactionTypeClassificationForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_type_classification_create'),
            'list_url': reverse('transaction_type_classification_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_type_classification_list(request):
    screen_name = 'Transaction Type Classification'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','TransactionTypeClassification'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in TransactionTypeClassification._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('transaction_type_classification_create'),
        'list_url': reverse('transaction_type_classification_list'),
        'update_url': 'transaction-type-classification-update',
        'delete_url': 'transaction-type-classification-delete',
        'add_new':'yes',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_type_mode_create(request):
    screen_name = 'Transaction Type Mode'
    if request.method == 'POST':
        form = TransactionTypeModeForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            form_obj.save()
            resp = tenant_create_save(form_obj,request.user) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('transaction_type_mode_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('transaction_type_mode_create'),
                'list_url': reverse('transaction_type_mode_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TransactionTypeModeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_type_mode_create'),
            'list_url': reverse('transaction_type_mode_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def transaction_type_mode_list(request):
    screen_name = 'Transaction Type Mode'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','TransactionTypeMode'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in TransactionTypeMode._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('transaction_type_mode_create'),
        'list_url': reverse('transaction_type_mode_list'),
        'update_url': 'transaction-type-mode-update',
        'delete_url': 'transaction-type-mode-delete',
        'add_new':'yes',
        'is_action_required': True,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def reference_type_create(request):
    screen_name = 'Reference Type'
    if request.method == 'POST':
        form = ReferenceTypeForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('reference_type_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('reference_type_create'),
                'list_url': reverse('reference_type_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = ReferenceTypeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('reference_type_create'),
            'list_url': reverse('reference_type_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def reference_type_list(request):
    screen_name = 'Reference Type'
    obj = ReferenceType.objects.all()
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','ReferenceType'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in ReferenceType._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('reference_type_create'),
        'list_url': reverse('reference_type_list'),
        'update_url': 'reference-type-update',
        'delete_url': 'reference-type-delete',
        'add_new':'yes',
        'is_action_required': True,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def payment_complexity_create(request):
    screen_name = 'Payment Complexity'
    if request.method == 'POST':
        form = PaymentComplexityForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('payment_complexity_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('payment_complexity_create'),
                'list_url': reverse('payment_complexity_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = PaymentComplexityForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('payment_complexity_create'),
            'list_url': reverse('payment_complexity_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def payment_complexity_list(request):
    screen_name = 'Payment Complexity'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','PaymentComplexity'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in PaymentComplexity._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('payment_complexity_create'),
        'list_url': reverse('payment_complexity_list'),
        'update_url': 'payment-complexity-update',
        'delete_url': 'payment-complexity-delete',
        'add_new':'no',
        'is_action_required': True,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)



@login_required(login_url='user_login')
def receivable_and_payable_transaction(request, special_txn):
    print('special_txn ', special_txn)
    screen_name = 'Receivable And Payable Transaction'
    if request.method == 'POST':
        form = PaymentAndReceiptForm(request.POST)
        if form.is_valid():
            transaction_type = request.POST.get('transaction_type')
            get_txn_obj = validate_transaction_type(transaction_type)
            print('error ...')
            if get_txn_obj is None:
                #messages.error(request, 'invalid txn type')
                return redirect(f'/rec-and-pay-transaction/{special_txn}')
            ## =========== Tenant Save Start =================
            # form_obj = form.save(commit=False)# enable because of using tenant save
            # resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            transaction_type_id = get_txn_obj.pk
            receivable = request.POST.get('receivable')
            payable = request.POST.get('payable')
            amount = eval(request.POST.get('amount'))
            if receivable == 'None' and payable == 'None':
                #messages.error(request, 'Receivable and payable should not be empty')
                return redirect(f'/rec-and-pay-transaction/{special_txn}')
            if str(get_txn_obj.name).lower() == 'payment' and payable == 'None':
                #messages.error(request, 'kindly select the payable')
                return redirect(f'/rec-and-pay-transaction/{special_txn}')
            if str(get_txn_obj.name).lower() == 'receipt' and receivable == 'None':
                #messages.error(request, 'kindly select the receivable')
                return redirect(f'/rec-and-pay-transaction/{special_txn}')
            # here logic for payable
            if str(get_txn_obj.name).lower() == 'payment':
                payable = apply_payment_to_payable(payable, amount)
                if not payable[0]:
                    #messages.error(request, f"""{payable[1]}""")
                    return redirect(f'/rec-and-pay-transaction/{special_txn}')
            # here logic for payable
            if str(get_txn_obj.name).lower() == 'receipt':
                payable = apply_payment_to_receivable(receivable, amount)
                if not payable[0]:
                    #messages.error(request, f"""{payable[1]}""")
                    return redirect(f'/rec-and-pay-transaction/{special_txn}')
            # Accounting Process
            account_category = get_txn_obj.category_of_account.account_category_id
            dr_obj = Accounts.objects.filter(account_category_id=account_category)
            if not dr_obj.exists():
                #messages.error(request, f"""Company account Not Founds""")
                return redirect(f'/rec-and-pay-transaction/{special_txn}')
            dr_obj_last = dr_obj.last()
            dr_acc = dr_obj_last.pk
            cr_acc = 16  # Just fixed credit acc id
            if str(get_txn_obj.name).lower() == 'receipt':
                cr_acc, dr_acc = dr_acc, cr_acc
            company_id = 'COMP--5524'
            logged_user_details = request.user.company_name
            company_id = logged_user_details.company_name
            local_currency_name = logged_user_details.local_currency
            local_currency_id = logged_user_details.local_currency.pk
            teller_profile = TellerProfile.objects.get(user=request.user)
            transaction_type = get_txn_obj.name
            is_teller = teller_profile.can_process_transaction(float(amount), str(transaction_type).lower())
            if not is_teller[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": is_teller[1]
                }
                template_name = 'pesanile_accounting/receivable_and_payable_transaction.html'
                return render(request, template_name, context)
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                            base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": get_ex_rate[1]
                }
                template_name = 'pesanile_accounting/receivable_and_payable_transaction.html'
                return render(request, template_name, context)
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
                                            status='pending',
                                            user=request.user,
                                            company=request.user.company_name,branch=request.user.branch_name)
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                                 credit_currency=local_currency_id,
                                 total_debit_amt=float(amount), debit_currency=local_currency_id,
                                 dr_acc=dr_acc,
                                 cr_acc=cr_acc,
                                 debit_credit_marker='DebitCredit', user=request.user.pk,
                                 company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                 )
            # form_obj = form.save(commit=False)
            obj.transaction_id = transaction_id
            obj.exchange_rate_calc_mode = res_cal_mode
            obj.exchange_rate_used_id = ex_rate_id
            obj.to_amount = amount
            obj.status = 'success' if resp else 'pending'
            obj.save()
            #messages.success(request, 'Success')
            # update the teller
            is_cleared = teller_profile.clear_teller_amount(float(amount), str(transaction_type))
            return redirect('transaction_list')

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('transaction_create'),
                'list_url': reverse('transaction_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/receivable_and_payable_transaction.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        get_txn_obj = validate_transaction_type(special_txn)
        if get_txn_obj is None:
            return redirect('transaction_create')
        # txn_obj = TransactionType.objects.get(pk=special_txn)
        form = PaymentAndReceiptForm(initial={
            'transaction_type': get_txn_obj.pk
        })
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_create'),
            'list_url': reverse('transaction_list'),
        }
        template_name = 'pesanile_accounting/receivable_and_payable_transaction.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def user_financial_accounting_mapping_create(request):
    screen_name = 'User Financial Account Mapping'
    if request.method == 'POST':
        form = UserFinancialAccountMappingForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('user_financial_accounting_mapping_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('user_financial_accounting_mapping_create'),
                'list_url': reverse('user_financial_accounting_mapping_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = UserFinancialAccountMappingForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('user_financial_accounting_mapping_create'),
            'list_url': reverse('user_financial_accounting_mapping_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def user_financial_accounting_mapping_list(request):
    screen_name = 'User Financial Account Mapping'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','UserFinancialAccountMapping'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in UserFinancialAccountMapping._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('user_financial_accounting_mapping_create'),
        'list_url': reverse('user_financial_accounting_mapping_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def user_financial_accounting_category_create(request):
    screen_name = 'User Financial Account Category'
    if request.method == 'POST':
        form = UserFinancialAccountCategoryForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('user_financial_accounting_category_list')
        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('user_financial_accounting_category_create'),
                'list_url': reverse('user_financial_accounting_category_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = UserFinancialAccountCategoryForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('user_financial_accounting_category_create'),
            'list_url': reverse('user_financial_accounting_category_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def user_financial_accounting_category_list(request):
    screen_name = 'User Financial Account Category'
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','UserFinancialAccountCategory'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in UserFinancialAccountCategory._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('user_financial_accounting_category_create'),
        'list_url': reverse('user_financial_accounting_category_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)
def check_charge_code_attached_or_not(get_txn_obj,actual_amount):
    try:
        charge = get_txn_obj.charge_code
        if charge.exists():
            print('charge ',charge)
            obj = charge.all()
            data_list = []
            total_amount = 0
            print('actual_amount ',actual_amount)
            for o in obj:
                gl_line_to_credit = o.gl_line_to_credit
                transaction_code_to_use = o.transaction_code_to_use
                charge_mode = o.charge_mode
                charge_amount = o.charge_amount
                data = {
                    'gl_line_to_credit': Accounts.objects.get(gl_line=gl_line_to_credit),
                    'transaction_code_to_use':transaction_code_to_use,
                    'charge_mode':charge_mode,
                    'charge_amount':charge_amount,
                }
                if charge_mode == 'flat':
                    amt = charge_amount
                if charge_mode == 'percentage':
                    amt = (actual_amount*charge_amount)/100
                total_amount = total_amount + amt
                data_list.append(data)
            print('total_amount ',total_amount)
            return [True,data_list,total_amount]
        else:
            return [False,'Charge is not exists']
    except Exception as error:
        print('error :',error)
        return [False, f'''{error}''']
    
@login_required(login_url='user_login')
def post_receivable_and_payable_transaction(request):
    screen_name = 'Post Receivable And Payable Transaction'
    is_credit_partial_txn = False
    if request.method == 'POST':
        form = PostPaymentAndReceiptForm(request.POST)
        print('im here..')
        if form.is_valid():
            transaction_for = request.GET.get('transaction_type')
            print('transaction_for',transaction_for)
            transaction_type = request.POST.get('transaction_type_name')
            special_txn = request.POST.get('transaction_type')
            get_txn_obj = validate_transaction_type(transaction_type)
            print('special_txn ',special_txn)
            if get_txn_obj is None:
                #messages.error(request, 'invalid txn type')
                return redirect(f'/rec-and-pay-transaction/{special_txn}')
            transaction_type_id = get_txn_obj.pk
            reference_number = request.POST.get('reference_number')
            receivable = request.POST.get('receivable')
            payable = request.POST.get('payable')
            amount = payment_amount = eval(request.POST.get('amount'))
            # here logic for payable
            print('here...',str(get_txn_obj.name).lower())
            if transaction_for == 'payment':
                payable = apply_payment_to_payable(reference_number, amount)
                print('payable ',payable)
                if not payable[0]:
                    print('payable[0] ',payable[0])
                    #messages.error(request, f"""{payable[1]}""")
                    return redirect(f'/rec-and-pay-transaction/{special_txn}')
                payable_obj = rec_pay_obj = AccountPayable.objects.get(reference_number=reference_number)
                payment_status = rec_pay_payment_status = payable_obj.payment_status
                actual_amount = payable_obj.actual_amount
                if amount < 1:
                    amount = actual_amount
                amount_paid = payable_obj.amount_paid
                cal_amt = amount + amount_paid
                if actual_amount == amount and amount_paid == 0:
                    payment_status = 'paid'
                if actual_amount > amount:
                    if cal_amt >= actual_amount:
                        payment_status = 'paid'
                    else:
                        payment_status = 'partially_paid'
                print('payment_status ', payment_status)
            print('Im here...')
            # here logic for payable
            if transaction_for == 'receipt':
                payable = apply_payment_to_receivable(reference_number, amount)
                if not payable[0]:
                    #messages.error(request, f"""{payable[1]}""")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))            # Accounting Process
                receivable_obj = rec_pay_obj = AccountReceivable.objects.get(reference_number=reference_number)
                print('receivable_obj.payment_status ',receivable_obj.payment_status)
                payment_status = rec_pay_payment_status = str(receivable_obj.payment_status)
                print('rec_pay_payment_status ',rec_pay_payment_status)
                actual_amount = receivable_obj.actual_amount
                if amount < 1:
                    amount = actual_amount
                if 1 <= amount < actual_amount and payment_status == 'unpaid':
                    bank_amount = amount
                    receivable_amount = actual_amount - bank_amount
                    # amount = actual_amount
                    is_credit_partial_txn = True
                    receivable_debit = amount
                    bank_acc_obj = Accounts.objects.filter(short_description__icontains='Bank Account')
                    if not bank_acc_obj.exists():
                        context = {
                            'form': form,
                            'screen_name': screen_name,
                            'create_url': reverse('transaction_create'),
                            'list_url': reverse('transaction_list'),
                            "message": "Bank account is not found , kindly configure that name should be Bank Account"
                        }
                        template_name = 'pesanile_accounting/post_receivable_and_payable_transaction.html'
                        return render(request, template_name, context)
                    last_bank_acc_obj = bank_acc_obj.last()
                    bank_account = last_bank_acc_obj.pk
                    # return
                amount_paid = receivable_obj.amount_received
                cal_amt = amount + amount_paid
                if actual_amount == amount and amount_paid == 0:
                    if payment_amount < 1:
                        payment_status = 'partially_paid'
                    else:
                        payment_status = 'paid'
                if actual_amount > amount:
                    print('paid , partially')
                    if cal_amt >= actual_amount:
                        payment_status = 'paid'
                        print('paid')
                    else:
                        print('partiall paid')
                        payment_status = 'partially_paid'

            account_category = get_txn_obj.category_of_account.account_category_id
            dr_obj = Accounts.objects.filter(account_category_id=account_category)
            if not dr_obj.exists():
                #messages.error(request, f"""Company account Not Founds""")
                return redirect(f'/rec-and-pay-transaction/{special_txn}')
            dr_obj_last = dr_obj.last()
            dr_acc = dr_obj_last.pk
            cr_acc = 'AC-1675'  # Just fixed credit acc id
            if str(get_txn_obj.name).lower() == 'receipt':
                cr_acc, dr_acc = dr_acc, cr_acc
            logged_user_details = request.user
            # company_id = logged_user_details.company_name
            company_id = 'COMP--5524'
            company_id = company_id
            local_currency_name = 'KSH'
            local_currency_id = 'shelling-8837'
            transaction_type = get_txn_obj.name
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                            base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": get_ex_rate[1]
                }
                template_name = 'pesanile_accounting/receivable_and_payable_transaction.html'
                return render(request, template_name, context)
            res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
            txn_type_obj = TransactionType.objects.get(name=transaction_type)
            dr_txn_code = txn_type_obj.debit_transaction_code
            cr_txn_code = txn_type_obj.credit_transaction_code
            credit_amount = float(amount) * float(ex_rate)
            entry_type = 'PL'
            transaction_id = generate_txn_id()
            dr_cur_list = eval(get_txn_obj.debit_currency)
            dr_acc_list = eval(get_txn_obj.debit_account)
            cr_cur_list = eval(get_txn_obj.credit_currency)
            cr_acc_list = eval(get_txn_obj.credit_account)
            resp = check_charge_code_attached_or_not(get_txn_obj, actual_amount)
            print('resp ',resp)
            if resp[0]:
                total_charge_amount = resp[2]
                print('amount ',amount)
                print('total_charge_amount ',total_charge_amount)
            else:
                total_charge_amount = 0
            print('is_credit_partial_txn ',is_credit_partial_txn)
            if is_credit_partial_txn:
                resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                     credit_amount=0,
                                     credit_currency=local_currency_id,
                                     total_debit_amt=float(bank_amount), debit_currency=local_currency_id,
                                     dr_acc=bank_account,
                                     cr_acc=None,
                                     debit_credit_marker='Debit', user=request.user.pk,
                                     company=request.user.company_name, ref_no=reference_number,
                                     branch=request.user.branch_name,
                                     )
                for dr_cur, dr_acc, cr_cur, cr_acc in zip(dr_cur_list, dr_acc_list, cr_cur_list, cr_acc_list):
                    obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id,
                                                    amount,
                                                    cr_acc,
                                                    local_currency_id, amount, res_cal_mode, ex_rate_id,
                                                    charges_applied=False,
                                                    status='pending',
                                                    user=request.user,
                                                    company=request.user.company_name, branch=request.user.branch_name)
                    resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                         credit_amount=actual_amount - total_charge_amount,
                                         credit_currency=local_currency_id,
                                         total_debit_amt=float(receivable_amount), debit_currency=local_currency_id,
                                         dr_acc=dr_acc,
                                         cr_acc=cr_acc,
                                         debit_credit_marker='DebitCredit', user=request.user.pk,
                                         company=request.user.company_name, ref_no=reference_number,
                                         branch=request.user.branch_name,
                                         )
            else:
                for dr_cur, dr_acc, cr_cur, cr_acc in zip(dr_cur_list, dr_acc_list, cr_cur_list, cr_acc_list):
                    obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id,
                                                    amount,
                                                    cr_acc,
                                                    local_currency_id, amount, res_cal_mode, ex_rate_id,
                                                    charges_applied=False,
                                                    status='pending',
                                                    user=request.user,
                                                    )
                    resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                         credit_amount=amount - total_charge_amount,
                                         credit_currency=local_currency_id,
                                         total_debit_amt=float(amount), debit_currency=local_currency_id,
                                         dr_acc=dr_acc,
                                         cr_acc=cr_acc,
                                         debit_credit_marker='DebitCredit', user=request.user.pk,
                                          ref_no=reference_number,
                                         )
            # Entry for charge
            if rec_pay_payment_status == 'unpaid':
                resp = check_charge_code_attached_or_not(get_txn_obj,actual_amount)
                if resp[0]:
                    for data_dict in resp[1]:
                        gl_line_to_credit = data_dict.get('gl_line_to_credit')
                        transaction_code_to_use = data_dict.get('transaction_code_to_use')
                        charge_mode = data_dict.get('charge_mode')
                        charge_amount = data_dict.get('charge_amount')
                        if charge_mode == 'flat':
                            total_amount = charge_amount
                        if charge_mode == 'percentage':
                            total_amount = (actual_amount * charge_amount) / 100
                        resp = account_entry(entry_type, transaction_id, transaction_code_to_use, transaction_code_to_use, credit_amount=total_amount,
                                             credit_currency=local_currency_id,
                                             total_debit_amt=float(total_amount), debit_currency=local_currency_id,
                                             dr_acc=dr_acc,
                                             cr_acc=gl_line_to_credit.pk,
                                             debit_credit_marker='Credit', user=request.user.pk,
                                             company=request.user.company_name, ref_no=reference_number,
                                             branch=request.user.branch_name,
                                             )
            # form_obj = form.save(commit=False)
            # obj.transaction_id = transaction_id
            # obj.exchange_rate_calc_mode = res_cal_mode
            # obj.exchange_rate_used_id = ex_rate_id
            # obj.to_amount = amount
            # obj.status = 'success' if resp else 'pending'
            # obj.save()
            # #messages.success(request, 'Success')
            # debit less and credit plus
            obj.transaction_id = transaction_id
            obj.exchange_rate_calc_mode = res_cal_mode
            obj.exchange_rate_used_id = ex_rate_id
            obj.to_amount = payment_amount
            obj.status = 'success' if resp else 'pending'
            obj.save()
            # update the payment status
            print('rec_pay_payment_status ',rec_pay_payment_status)
            print('payment_status ',payment_status)
            print('str(get_txn_obj.name).lower() ',str(get_txn_obj.name).lower())
            if str(transaction_for).lower() == 'receipt':
                receivable = receivable_atomic(reference_number, payment_amount,
                                               company_id=request.user.company_name,
                                               branch=request.user.branch_name)
                print('receivable ',receivable)
                receivable.payment_status = payment_status
                receivable.save()
            if str(transaction_for).lower() == 'payment':
                payment = payment_atomic(reference_number, payment_amount)
                payment.payment_status = payment_status
                payment.save()
            # update the payment status
            return redirect('transaction_list')

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('transaction_create'),
                'list_url': reverse('transaction_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/post_receivable_and_payable_transaction.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        print('here')
        reference_number = request.GET.get('reference_number')
        transaction_type = request.GET.get('transaction_type')
        print('transaction_type ',transaction_type)
        # get_txn_obj = TransactionType.objects.filter(name__iexact=transaction_type)
        records = TransactionType.objects.all()
        # print('not ',get_txn_obj)
        print('======================')
        # if not get_txn_obj.exists():
        #     return redirect('account_receivable_list')
        # get payable and receivable details
        get_details = get_receivable_and_payable_details(reference_number, transaction_type)
        if not get_details[0]:
            return redirect('account_receivable_list')
        initial = {
            'amount': get_details[1].amount_due,
            'reference_number': get_details[1].reference_number,

        }
        print('initial ',initial)
        form = PostPaymentAndReceiptForm(initial={
            'transaction_type': 1,
            'amount': get_details[1].amount_due,
            'reference_number': get_details[1].reference_number,

        })
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('transaction_create'),
            'list_url': reverse('transaction_list'),
            'transaction_type':transaction_type,
            'records':records
        }
        print('transaction_type ',transaction_type)
        print('its okayhere...')
        template_name = 'pesanile_accounting/post_receivable_and_payable_transaction.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def account_payment_create(request):
    screen_name = 'Direct Payment'
    if request.method == 'POST':
        form = AccountPaymentForm(request.POST)
        if form.is_valid():
            transaction_type = request.POST.get('transaction_type', 'payment')

            get_txn_obj = get_txn_type_by_name('payment')
            print('error ...', get_txn_obj)
            if get_txn_obj is None:
                #messages.error(request, 'invalid txn type')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            #             # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            transaction_type_id = get_txn_obj.pk
            reference_number = request.POST.get('reference_number')
            amount = eval(request.POST.get('amount'))
            account_category = get_txn_obj.category_of_account.account_category_id
            dr_obj = Accounts.objects.filter(account_category_id=account_category)
            if not dr_obj.exists():
                #messages.error(request, f"""Company account Not Founds""")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            dr_obj_last = dr_obj.last()
            dr_acc = dr_obj_last.pk
            cr_acc = 16  # Just fixed credit acc id
            if str(get_txn_obj.name).lower() == 'receipt':
                cr_acc, dr_acc = dr_acc, cr_acc
            company_id = 'COMP--5524'
            logged_user_details = request.user.company_name
            company_id = logged_user_details.company_name
            local_currency_name = logged_user_details.local_currency
            local_currency_id = logged_user_details.local_currency.pk
            teller_profile = TellerProfile.objects.get(user=request.user)
            transaction_type = get_txn_obj.name
            is_teller = teller_profile.can_process_transaction(float(amount), str(transaction_type).lower())
            if not is_teller[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": is_teller[1]
                }
                template_name = 'pesanile_accounting/receivable_and_payable_transaction.html'
                return render(request, template_name, context)
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                            base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": get_ex_rate[1]
                }
                template_name = 'pesanile_accounting/receivable_and_payable_transaction.html'
                return render(request, template_name, context)
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
                                            status='pending',
                                            user=request.user,
                                            company=request.user.company_name,branch=request.user.branch_name)
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                                 credit_currency=local_currency_id,
                                 total_debit_amt=float(amount), debit_currency=local_currency_id,
                                 dr_acc=dr_acc,
                                 cr_acc=cr_acc,
                                 debit_credit_marker='DebitCredit', user=request.user.pk,
                                 company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                 )
            # form_obj = form.save(commit=False)
            obj.transaction_id = transaction_id
            obj.exchange_rate_calc_mode = res_cal_mode
            obj.exchange_rate_used_id = ex_rate_id
            obj.to_amount = amount
            obj.status = 'success' if resp else 'pending'
            obj.save()
            form_obj = form.save(commit=False)
            form_obj.transaction_id = transaction_id
            ## =========== Tenant Save Start =================
            # form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            # update the teller
            is_cleared = teller_profile.clear_teller_amount(float(amount), str(transaction_type))
            return redirect('direct_payment_list')

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('payment_create'),
                'list_url': reverse('payment_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountPaymentForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('payment_create'),
            'list_url': reverse('payment_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def account_receipt_create(request):
    screen_name = 'Direct Receipt'
    if request.method == 'POST':
        form = AccountReceiptForm(request.POST)
        if form.is_valid():
            transaction_type = request.POST.get('transaction_type', 'receipt')

            get_txn_obj = get_txn_type_by_name('receipt')
            print('error ...', get_txn_obj)
            if get_txn_obj is None:
                #messages.error(request, 'invalid txn type')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            ## =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            transaction_type_id = get_txn_obj.pk
            reference_number = request.POST.get('reference_number')
            amount = eval(request.POST.get('amount'))
            account_category = get_txn_obj.category_of_account.account_category_id
            dr_obj = Accounts.objects.filter(account_category_id=account_category)
            if not dr_obj.exists():
                #messages.error(request, f"""Company account Not Founds""")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
            dr_obj_last = dr_obj.last()
            dr_acc = dr_obj_last.pk
            cr_acc = 16  # Just fixed credit acc id
            if str(get_txn_obj.name).lower() == 'receipt':
                cr_acc, dr_acc = dr_acc, cr_acc
            company_id = 'COMP--5524'
            logged_user_details = request.user.company_name
            company_id = logged_user_details.company_name
            local_currency_name = logged_user_details.local_currency
            local_currency_id = logged_user_details.local_currency.pk
            teller_profile = TellerProfile.objects.get(user=request.user)
            transaction_type = get_txn_obj.name
            # is_teller = teller_profile.can_process_transaction(float(amount), str(transaction_type).lower())
            # if not is_teller[0]:
            #     context = {
            #         'form': form,
            #         'screen_name': screen_name,
            #         'create_url': reverse('transaction_create'),
            #         'list_url': reverse('transaction_list'),
            #         "message": is_teller[1]
            #     }
            #     template_name = 'pesanile_accounting/create_everything.html'
            #     return render(request, template_name, context)
            get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                            base_currency=str(local_currency_name))
            if not get_ex_rate[0]:
                context = {
                    'form': form,
                    'screen_name': screen_name,
                    'create_url': reverse('transaction_create'),
                    'list_url': reverse('transaction_list'),
                    "message": get_ex_rate[1]
                }
                template_name = 'pesanile_accounting/create_everything.html'
                return render(request, template_name, context)
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
                                            status='pending',
                                            user=request.user,
                                            company=request.user.company_name,branch=request.user.branch_name
                                            )
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                                 credit_currency=local_currency_id,
                                 total_debit_amt=float(amount), debit_currency=local_currency_id,
                                 dr_acc=dr_acc,
                                 cr_acc=cr_acc,
                                 debit_credit_marker='DebitCredit', user=request.user.pk,
                                 company=request.user.company_name, ref_no=None, branch=request.user.branch_name
                                 )
            # form_obj = form.save(commit=False)
            obj.transaction_id = transaction_id
            obj.exchange_rate_calc_mode = res_cal_mode
            obj.exchange_rate_used_id = ex_rate_id
            obj.to_amount = amount
            obj.status = 'success' if resp else 'pending'
            obj.save()
            form_obj = form.save(commit=False)
            form_obj.transaction_id = transaction_id
            ## =========== Tenant Save Start =================
            # form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            # update the teller
            is_cleared = teller_profile.clear_teller_amount(float(amount), str(transaction_type))
            return redirect('direct_receipt_list')

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
                'create_url': reverse('receipt_create'),
                'list_url': reverse('receipt_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountReceiptForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('receipt_create'),
            'list_url': reverse('receipt_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)




@login_required(login_url='user_login')
def direct_receipt_list(request):
    screen_name = "Direct Receipt"
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','AccountReceipt'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in AccountReceipt._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_receipt_create'),
        'list_url': reverse('direct_receipt_list'),
        'add_new':'no',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)

@login_required(login_url='user_login')
def direct_payment_list(request):
    screen_name = "Direct Payment"
    obj = AccountPayment.objects.all()
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','AccountPayment'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in AccountPayment._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('account_payment_create'),
        'list_url': reverse('direct_payment_list'),
        'add_new': 'no',
        'is_action_required': False,
    }
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


# custom field and their types


@login_required(login_url='user_login')
def custom_field_type_create(request):
    screen_name = 'Custom Field Type'
    if request.method == 'POST':
        form = CustomFieldTypeForm(request.POST)
        if form.is_valid():
            # =========== Pre Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            resp = pre_setup_tenant_create_save(form_obj, request.user)  # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('custom_field_type_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('custom_field_type_create'),
                'list_url': reverse('custom_field_type_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CustomFieldTypeForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('custom_field_type_create'),
            'list_url': reverse('custom_field_type_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def custom_field_type_list(request):
    screen_name = "Custom Field Type"
    obj = CustomFieldType.objects.all()
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','CustomFieldType'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in CustomFieldType._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('custom_field_type_create'),
        'list_url': reverse('custom_field_type_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)



@login_required(login_url='user_login')
def custom_field_create(request):
    screen_name = 'Custom Field '
    if request.method == 'POST':
        form = CustomFieldForm(request.POST)
        if form.is_valid():
            # =========== Pre Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            form_obj.save()
            resp = pre_setup_tenant_create_save(form_obj, request.user)  # Pre setup Tenant Save
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('custom_field_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('custom_field_create'),
                'list_url': reverse('custom_field_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CustomFieldForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('custom_field_create'),
            'list_url': reverse('custom_field_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def custom_field_list(request):
    screen_name = "Custom Field"
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','CustomField'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    print('obj ',obj)
    # ========= End filter role based data ================
    obj_fields = [field for field in CustomField._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('custom_field_create'),
        'list_url': reverse('custom_field_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)
def generate_custom_id(pre_fix):
    """
    Generates a unique transaction ID in the format TXN-YYYYMMDD-RANDOM.

    Returns:
        str: The generated transaction ID.
    """
    ids = f"{pre_fix}-" + f"{get_current_date()}-" + str(
        int(get_random_string(length=5, allowed_chars="1234567890")))
    return ids

@login_required(login_url='user_login')
def custom_transaction_field_mapping_create(request):
    screen_name = 'Custom Transaction Field Mapping'
    if request.method == 'POST':
        form = CustomTransactionFieldMappingForm(request.POST,created_by=request.user)
        if form.is_valid():
            print('REQUEST POST ',request.POST)
            company = request.user.company_name
            transaction_type = request.POST.get('transaction_type')
            field_name = request.POST.getlist('field_name')
            field_type = request.POST.getlist('field_type')
            is_required = request.POST.getlist('is_required')
            if len(field_name) != len(is_required):
                is_required.insert(0,False)
            identification_key = generate_custom_id(pre_fix='IDK')
            for field_name, field_type, is_required in zip(field_name, field_type, is_required,):
                obj = CustomTransactionFieldMapping.objects.create(
                    company_name=company,
                    transaction_type_id=transaction_type,
                    field_name_id=field_name,
                    field_type_id=field_type,
                    is_required= True if is_required == 'on' else False,
                    identification_key=identification_key,
                    created_by_id=request.user.pk,
                )
                print('obj ',obj)
            #messages.success(request, 'Success')
            return redirect('custom_transaction_field_mapping_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('custom_transaction_field_mapping_create'),
                'list_url': reverse('custom_transaction_field_mapping_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/custom_transaction_field_mapping_create.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CustomTransactionFieldMappingForm(created_by=request.user)
        field_obj = CustomField.objects.all()
        field_type_obj = CustomFieldType.objects.all()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('custom_transaction_field_mapping_create'),
            'list_url': reverse('custom_transaction_field_mapping_list'),
            'field_obj':field_obj,'field_type_obj':field_type_obj,
        }
        template_name = 'pesanile_accounting/custom_transaction_field_mapping_create.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def custom_transaction_field_mapping_list(request):
    screen_name = 'Custom Transaction Field Mapping'
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','CustomTransactionFieldMapping'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in CustomTransactionFieldMapping._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('custom_transaction_field_mapping_create'),
        'list_url': reverse('custom_transaction_field_mapping_list'),
        'add_new':'yes',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def custom_transaction_detail_list(request):
    screen_name = 'Custom Transaction Detail'
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','CustomTransactionDetail'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in CustomTransactionDetail._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'add_new': 'no',
        'create_url': reverse('custom_transaction_field_mapping_create'),
        'list_url': reverse('custom_transaction_field_mapping_list'),
        'add_new':'no',
        'is_action_required': False,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


def bank_detail_list(request):
    # bank_details = BankRegistration.objects.all()
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','BankRegistration'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    return render(request, 'pesanile_accounting/bank_detail_list.html', {'bank_details': obj})

# Create View
def bank_detail_create(request):
    if request.method == 'POST':
        form = BankRegistrationForm(request.POST)
        if form.is_valid():
                        # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            return redirect('bank_detail_list')
        # api_resp = api_post(URL_ACCOUNT_CREATE, data=my_dict)
        # print('api_resp ',api_resp)

    else:
        form = BankRegistrationForm()
    return render(request, 'pesanile_accounting/bank_detail_form.html', {'form': form})

# Update View
def bank_detail_update(request, pk):
    bank_detail = get_object_or_404(BankRegistration, pk=pk)
    if request.method == 'POST':
        form = BankRegistrationForm(request.POST, instance=bank_detail)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)# enable because of using tenant save
            resp = tenant_create_save(form_obj,request.user, request.user.company_name,request.user.branch_name) # Tenant Save
            # =========== Tenant Save End =================
            return redirect('bank_detail_list')
    else:
        form = BankRegistrationForm(instance=bank_detail)
    return render(request, 'pesanile_accounting/bank_detail_form.html', {'form': form})

# Delete View
def bank_detail_delete(request, pk):
    bank_detail = get_object_or_404(BankRegistration, pk=pk)
    bank_detail.delete()
    return render(request, 'pesanile_accounting/bank_detail_confirm_delete.html', {'bank_detail': bank_detail})


@login_required(login_url='user_login')
def business_group_create(request):
    screen_name = 'Business Group'
    if request.method == 'POST':
        form = BusinessGroupForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            form_obj.created_by=request.user
            form_obj.updated_by=request.user
            form_obj.save()
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('business_group_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('business_group_create'),
                'list_url': reverse('business_group_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = BusinessGroupForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('business_group_create'),
            'list_url': reverse('business_group_list'),
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def business_group_list(request):
    screen_name = "Business Group"
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','BusinessGroup'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in BusinessGroup._meta.get_fields() if exclude_field(field.name)]
    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('business_group_create'),
        'list_url': reverse('business_group_list'),
        'add_new':'yes',
        'is_action_required': False,
    }

    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


@login_required(login_url='user_login')
def department_create(request):
    screen_name = 'Department'
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            # =========== Tenant Save Start =================
            form_obj = form.save(commit=False)  # enable because of using tenant save
            form_obj.created_by=request.user
            form_obj.updated_by=request.user
            form_obj.save()
            # =========== Tenant Save End =================
            #messages.success(request, 'Success')
            return redirect('department_list')
        else:
            context = {
                'form': form,
                'create_url': reverse('department_create'),
                'list_url': reverse('department_list'),
                "message": "TECHNICAL ERROR WHILE CREATING"
            }
            template_name = 'pesanile_accounting/create_everything.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = DepartmentForm()
        context = {
            'form': form,
            'screen_name': screen_name,
            'create_url': reverse('department_create'),
            'list_url': reverse('department_list'),
            'add_new':'yes',
            'is_action_required': False,
        }
        template_name = 'pesanile_accounting/create_everything.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def department_list(request):
    screen_name = "Department"
    # ========= Start filter role based data =============
    app_name, model_name = 'pesanile_accounting','Department'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    obj_fields = [field for field in Department._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('department_create'),
        'list_url': reverse('department_list'),
        'add_new':'yes',
        'is_action_required': False,
    }

    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)


def account_creation_finance(account_holder,short_description):
    print('account_holder',account_holder)
    total_account = Accounts.objects.filter(created_at__date=datetime.datetime.today().date())
    gl_line=GLLine.objects.get(name='Funds Transfer')
    print('gl_line',gl_line.pk)
    account_type=AccountType.objects.get(name='Equity')
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