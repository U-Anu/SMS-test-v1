from django.shortcuts import render, redirect
from .forms import *
from .scripts import *
from pesanile_accounting.models import AccountEntry, AccountReceivable, AccountPayable, Receipt, Payment
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required



# Create your views here.
@login_required(login_url='/')
def date_wise(request):
    screen_name = 'Date Wise Report'
    if request.method == 'POST':
        form = DateWiseForm(request.POST)
        if form.is_valid():
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            obj = date_wise_report(start_date, end_date)
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = { 
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = DateWiseForm()
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)


# Create your views here.
@login_required(login_url='/')
def transaction_id_wise(request):
    screen_name = 'Transaction Id Wise Report'
    if request.method == 'POST':
        form = TransactionIdForm(request.POST)
        if form.is_valid():
            print("for transacrion")
            transaction_id = request.POST.get('transaction_id')
            print("for  type",transaction_id)
            obj = transaction_id_wise_report(str(transaction_id))
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TransactionIdForm()
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def account_wise(request):
    screen_name = 'Account Wise Report'
    if request.method == 'POST':
        form = AccountWiseReportForm(request.POST)
        if form.is_valid():
            transaction_id = request.POST.get('account_number')
            obj = account_wise_report(str(transaction_id))
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = AccountWiseReportForm()
        print('form ', form)
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def transaction_journal(request):
    screen_name = 'Transaction journal'
    if request.method == 'POST':
        form = transaction_journalReportForm(request.POST)
        form1 = DateWiseForm(request.POST)
        if form.is_valid():
            transaction_id = request.POST.get('account_number',None)
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            print('start_date',start_date)
            print('end_date',end_date)  
            print('account',transaction_id)  
            obj = TJ_wise_report(str(transaction_id),start_date,end_date)
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'form1': form1,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports_TJ.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'form1': form1,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports_TJ.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = transaction_journalReportForm()
        form1 = DateWiseForm()
        print('form ', form)
        context = {
            'form': form,
            'form1': form1,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports_TJ.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def teller_wise(request):
    screen_name = 'Teller Wise Report'
    if request.method == 'POST':
        form = TellerWiseReportForm(request.POST)
        if form.is_valid():
            teller = request.POST.get('teller')
            obj = teller_wise_report(str(teller))
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TellerWiseReportForm()
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def transaction_code_wise(request):
    screen_name = 'Transaction Code Wise Report'
    if request.method == 'POST':
        form = TransactionCodeWiseReportForm(request.POST)
        if form.is_valid():
            transaction_code = request.POST.get('transaction_code')
            print('transaction_code ', transaction_code)
            obj = transaction_code_wise_report(str(transaction_code))
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TransactionCodeWiseReportForm()
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def till_wise(request):
    screen_name = 'Till Wise Report'
    if request.method == 'POST':
        form = TillWiseReportForm(request.POST)
        if form.is_valid():
            till_code = request.POST.get('till_code')
            print('till_code ', till_code)
            obj = till_wise_report(str(till_code))
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TillWiseReportForm()
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)


@login_required(login_url='/')
def dutymeal_wise(request):
    screen_name = 'Duty Meal Wise Report'
    if request.method == 'POST':
        form = DutyMealWiseReportForm(request.POST)
        if form.is_valid():
            dutymeal_id = request.POST.get('dutymeal_id')
            print('dutymeal_id ', dutymeal_id)
            obj = dutymeal_wise_report(str(dutymeal_id))
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = DutyMealWiseReportForm()
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)
    

@login_required(login_url='/')
def company_wise(request):
    screen_name = 'Company Wise Report'
    if request.method == 'POST':
        form = CompanyWiseReportForm(request.POST)
        if form.is_valid():
            company = request.POST.get('company')
            print('company ', company)
            obj = company_wise_report(str(company))
            obj_fields = AccountEntry._meta.get_fields()
            print('obj ', obj)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = CompanyWiseReportForm()
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)


# ============= Advance Reports =============================
@login_required(login_url='/')
def trail_balance(request):
    screen_name = 'Trail Balance Report'
    if request.method == 'POST':
        form = TrailBalanceReportForm(request.POST)
        if form.is_valid():
            account_number = request.POST.get('account_number')
            obj = account_wise_report(str(account_number))
            obj_fields = AccountEntry._meta.get_fields()

            # Define the fields you want to exclude
            exclude_fields = ['id', 'entry_type', 'user', 'exposure_date', 'posting_date']

            # Filter out the excluded fields
            obj_fields = [field for field in obj_fields if field.name not in exclude_fields]
            total_debit = obj.filter(debit_credit_marker='Debit').aggregate(Sum('amount'))
            print('total_debit ', total_debit)
            total_credit = obj.filter(debit_credit_marker='Credit').aggregate(Sum('amount'))
            print('total_credit ', total_credit)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
                'enable_extra': True,
                'total_debit': total_debit.get('amount__sum'), 'total_credit': total_credit.get('amount__sum'),
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = TrailBalanceReportForm()
        print('form ', form)
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def glline_with_different_sub_glline(request):
    screen_name = 'GL Line Report'
    if request.method == 'POST':
        form = GLLineReportForm(request.POST)
        if form.is_valid():
            glline = request.POST.get('glline')
            obj = glline_with_different_sub_glline_wise_report(str(glline))
            obj_fields = AccountEntry._meta.get_fields()

            # Define the fields you want to exclude
            exclude_fields = ['id', 'entry_type', 'user', 'exposure_date', 'posting_date']

            # Filter out the excluded fields
            obj_fields = [field for field in obj_fields if field.name not in exclude_fields]
            total_debit = obj.filter(debit_credit_marker='Debit').aggregate(Sum('amount'))
            print('total_debit ', total_debit)
            total_credit = obj.filter(debit_credit_marker='Credit').aggregate(Sum('amount'))
            print('total_credit ', total_credit)
            context = {
                'form': form,
                'screen_name': screen_name,
                'obj_fields': obj_fields,
                'obj': obj,
                'enable_extra': True,
                'total_debit': total_debit.get('amount__sum'), 'total_credit': total_credit.get('amount__sum'),
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

        else:
            context = {
                'form': form,
                'screen_name': screen_name,
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)

    if request.method == 'GET':
        form = GLLineReportForm()
        print('form ', form)
        context = {
            'form': form,
            'screen_name': screen_name,
        }
        template_name = 'reports_acc/reports.html'
        return render(request, template_name, context)

# same as apis views

@login_required(login_url='/')
def trail_balance_report(request):
    try:
        if request.method == 'POST':
            form = TrailBalanceReportForm(data=request.POST)
            if form.is_valid():
                user_details = request.user
                company_id = user_details.company.pk
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                acc_obj = Accounts.objects.filter(company_id=company_id).only('account_number')
                my_list = []

                for data in acc_obj:
                    acc_ent_obj = AccountEntry.objects.filter(
                        Q(account_number=data) & Q(entry_date__range=(start_date, end_date)))
                    total_debit = acc_ent_obj.filter(debit_credit_marker='Debit').aggregate(Sum('amount')).get(
                        'amount__sum', 0) or 0
                    total_credit = acc_ent_obj.filter(debit_credit_marker='Credit').aggregate(Sum('amount')).get(
                        'amount__sum', 0) or 0

                    my_list.append({
                        'account_id': str(data.pk),
                        'account_number': str(data),
                        'debit_amount': total_debit,
                        'credit_amount': total_credit,
                    })
                context = {
                    'screen_name': 'Trail Balance',
                    'form':form,
                    'my_list': my_list,
                    'is_train_balance':True,
                }
                print('context ',context)
                template_name = 'reports_acc/reports.html'
                return render(request, template_name, context)

            context = {
                'form': form,
                'screen_name': 'Trail Balance'
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)
        else:
            form = TrailBalanceReportForm()
            context = {
                'form': form,
                'screen_name': 'Trail Balance'
            }
            template_name = 'reports_acc/reports.html'
            return render(request, template_name, context)
    except Exception as error:
        print('error ', error)
        messages.error(request, f"""{error}""")
        return redirect('trail_balance')

@login_required(login_url='/')
def general_ledger_with_diff_sub_ledgers(request):
    try:
        if request.method == 'GET':
            user_details = request.user
            company_id = None if user_details.company is None else user_details.company.pk
            acc_obj = Accounts.objects.filter(company_id=company_id).only('gl_line')
            my_list = []

            for data in acc_obj:
                acc_ent_obj = AccountEntry.objects.filter(account_number=data)
                for entry in acc_ent_obj:
                    my_list.append({
                        'account_id': str(entry.account_number.pk),
                        'account_number': str(entry.account_number),
                        'transaction_date': entry.entry_date.date(),
                        'amount': entry.amount,
                        'debit_credit_marker': entry.debit_credit_marker,
                    })

            context = {
                'my_list': my_list,
                'screen_name': 'General Ledger With Different Sub Ledgers'
            }
            template_name = 'reports_acc/general_ledger_with_diff_sub_ledgers.html'
            return render(request, template_name, context)

    except Exception as error:
        messages.error(request, f"""{error}""")
        return redirect('general_ledger_with_diff_sub_ledgers_report')


@login_required
def receivable_listing(request):
    if request.method == 'GET':
        user_details = request.user
        obj = AccountReceivable.objects.filter(company=request.user.company)
        context = {
            'obj':obj,
            'screen_name':'Receivable Listing'
        }
        template_name = 'reports_acc/receivable_listing.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def account_payable_listing(request):
    if request.method == 'GET':
        user_details = request.user
        company_id = None if user_details.company is None else user_details.company.pk
        obj = AccountPayable.objects.filter(company_id=company_id)
        context = {
            'obj' : obj,
            'screen_name':'Payable Listing'
        }
        template_name = 'reports_acc/account_payable_listing.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def statement_of_cash_flow(request):
    if request.method == 'GET':
        user_details = request.user
        company_id = None if user_details.company is None else user_details.company.pk
        acc_obj_expense = Accounts.objects.filter(Q(company_id=company_id) & Q(account_category__name='Expense'))
        acc_obj_income = Accounts.objects.filter(Q(company_id=company_id) & Q(account_category__name='Income'))
        my_list = []

        for data in acc_obj_expense:
            my_list.append({
                'account_id': data.account_id,
                'account_number': data.account_number,
                'amount': data.total_balance,
                'account_category': data.account_category.name,
                'type': 'Payment',
                'last_updated_at': data.updated_at.date()
            })

        for data in acc_obj_income:
            my_list.append({
                'account_id': data.account_id,
                'account_number': data.account_number,
                'amount': data.total_balance,
                'account_category': data.account_category.name,
                'type': 'Receipt',
                'last_updated_at': data.updated_at.date()
            })
        context = {
            'my_list' : my_list,
            'screen_name' : 'Statement Of Cash Flow'
        }
        template_name = 'reports_acc/statement_of_cash_flow.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def statement_of_receipt(request):
    if request.method == 'GET':
        user_details = request.user
        print('user_details ',user_details)
        company_id = None if user_details.company is None else user_details.company.pk
        print('company_id ',company_id)
        obj = Receipt.objects.filter(company_id=company_id)
        context = {
            'obj' : obj,
            'screen_name' : 'Statement of Receipt'
        }
        print('context ',context)
        template_name = 'reports_acc/statement_of_receipt.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def statement_of_payment(request):
    if request.method == 'GET':
        user_details = request.user
        company_id = None if user_details.company is None else user_details.company.pk
        obj = Payment.objects.filter(company_id=company_id)
        context = {
            'obj' : obj,
            'screen_name' : 'Statement of Payment'
        }
        template_name = 'reports_acc/statement_of_payment.html'
        return render(request, template_name, context)
