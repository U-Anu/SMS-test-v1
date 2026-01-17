from django.shortcuts import render, redirect
from .forms import *
from .scripts import *
from pesanile_accounting.models import AccountEntry, AccountReceivable, AccountPayable, Receipt, Payment
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .report_scripts import *


# Create your views here.
@login_required(login_url='user_login')
def trail_balance_report_views(request):
    if request.method == 'GET':
        data = trial_balance_report(company_name=None,branch_name=None)
        template_name = 'reports_acc/trail_balance_report.html'
        return render(request, template_name, data)

# Create your views here.
@login_required(login_url='user_login')
def general_ledger_report_views(request):
    if request.method == 'GET':
        data = general_ledger_report(company_name=None,branch_name=None)
        template_name = 'reports_acc/general_ledger_report.html'
        return render(request, template_name, data)

# Create your views here.
@login_required(login_url='user_login')
def generate_cash_flow_statement_views(request):
    screen_name = 'Cash flow statement'
    if request.method == 'GET':
        data = generate_cash_flow_statement(company_name=None,branch_name=None)
        context = {
            'cash_flow_statement':data,
            'screen_name':screen_name,
        }
        template_name = 'reports_acc/generate_cash_flow_statement.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def balance_sheet_views(request):
    screen_name = 'Balance sheet'
    if request.method == 'GET':
        data = balance_sheet(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/balance_sheet.html'
        return render(request, template_name, context)

# @login_required(login_url='user_login')
# def profit_and_loss_statement_views(request):
#     screen_name = 'Profit and loss statement'
#     if request.method == 'GET':
#         data = generate_balance_sheet()
#         context = {
#             'cash_flow_statement':data,
#             'screen_name':screen_name,
#         }
#         print('context',context)
#         template_name = 'reports/profit_and_loss_statement.html'
#         return render(request, template_name, context)

@login_required(login_url='user_login')
def profit_and_loss_statement_views(request):
    screen_name = 'Profit and loss statement'
    if request.method == 'GET':
        data = profit_and_loss(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/profit_and_loss_statement.html'
        return render(request, template_name, context)


@login_required(login_url='user_login')
def account_payable_aging_views(request):
    screen_name = 'Account payable aging'
    if request.method == 'GET':
        data = account_payable_aging(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/account_payable_aging.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def account_receivable_aging_views(request):
    screen_name = 'Account receivable aging'
    if request.method == 'GET':
        data = account_receivable_aging(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/account_receivable_aging.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def petty_cash_views(request):
    screen_name = 'Petty cash'
    if request.method == 'GET':
        data = petty_cash(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/petty_cash.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def trial_balance_by_period_views(request):
    screen_name = 'Trial balance by period'
    if request.method == 'GET':
        data = trial_balance_by_period(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/trial_balance_by_period.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def cash_book_detailed_report_all_views(request):
    screen_name = 'Cash book detailed report'
    if request.method == 'GET':
        data = cash_book_detailed_report_all(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/cash_book_detailed_report_all.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def accounts_payable_vs_receivable_summary_views(request):
    screen_name = 'Account payable vs receivable summary'
    if request.method == 'GET':
        data = accounts_payable_vs_receivable_summary(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/accounts_payable_vs_receivable_summary.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def petty_cash_usage_report_views(request):
    screen_name = 'Petty cash usage report'
    if request.method == 'GET':
        data = petty_cash_usage_report(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/petty_cash_usage_report.html'
        return render(request, template_name, context)

@login_required(login_url='user_login')
def journal_summary_report_views(request):
    screen_name = 'Journal summary report'
    if request.method == 'GET':
        data = journal_summary_report(company_name=None,branch_name=None)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/journal_summary_report_views.html'
        return render(request, template_name, context)


@login_required(login_url='/')
def balance_sheet_views_new(request):
    screen_name = 'Balance sheet'
    if request.method == 'POST':
        from_date=request.POST.get("from_date")
        to_date=request.POST.get("to_date")
        year_selection=request.POST.get("year_selection")
        print("from_date",from_date,'to_date',to_date,'year_selection',year_selection)
        data,cal_total = balance_sheet_new_new(company_name=None,branch_name=None,from_date=from_date,to_date=to_date,year_selection=year_selection)
        context = {
            'records':data,
            'cal_total':cal_total,
            'screen_name':screen_name,
        }    
    if request.method == 'GET':
        data,cal_total= balance_sheet_new_new(company_name=None,branch_name=None)
        context = {
            'records':data,
            'first':'first',
            'cal_total':cal_total,
            'screen_name':screen_name,
        }    
    template_name = 'reports_acc/balance_sheet_new_final.html'
    return render(request, template_name, context)


@login_required(login_url='/')
def profit_and_loss_statement_views_new(request):
    screen_name = 'Profit and Loss Statement'
    
    if request.method == 'GET':
        data,cal_total = profit_and_loss_new_new(company_name=None, branch_name=None)
       
        
        
        context = {
            'records': data,
            'cal_total': cal_total,
            'screen_name': screen_name,
        }
        # print('context', context)  # Debugging output
        template_name = 'reports_acc/profit_and_loss_statement_work.html'
        return render(request, template_name, context)



# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum
# import matplotlib.pyplot as plt
# import io
# import urllib, base64
# from pesanile_accounting.models import Accounts
# import matplotlib
# matplotlib.use('Agg')  
# import matplotlib.pyplot as plt

# @login_required(login_url='/')
# def budget_forecast_view(request):
#     screen_name = "Budget vs. Actual Report"

#     if request.method == 'GET':
#         data, total_budget, total_actual = get_budget_forecast_data(company=None)
#         chart_url = generate_budget_forecast_chart(data)
#         context = {
#             'records': data,
#             'total_budget': total_budget,
#             'total_actual': total_actual,
#             'chart_url': chart_url,
#             'screen_name': screen_name,
#         }
#         print('context',context)
#         return render(request, 'reports_acc/budget_forecast.html', context)

# def get_budget_forecast_data(company=None):
#     # Fetch accounts with budget and actual balances
#     accounts = Accounts.objects.all()
#     print('accounts',accounts)
#     final_data = []
#     total_budget = 0
#     total_actual = 0

#     for acc in accounts:
#         account_data = {
#             'account_name': acc.short_description,
#             'budgeted_amount': acc.opening_balance, 
#             'actual_amount': acc.total_balance 
#         }
#         total_budget += acc.opening_balance
#         total_actual += acc.total_balance
#         final_data.append(account_data)
#     return final_data, total_budget, total_actual

# def generate_budget_forecast_chart(data):
#     """ Generate a bar chart comparing actual vs. budgeted amounts. """
#     account_names = [d['account_name'] for d in data]
#     budgeted_amounts = [d['budgeted_amount'] for d in data]
#     actual_amounts = [d['actual_amount'] for d in data]

#     plt.figure(figsize=(10, 5))
#     plt.bar(account_names, budgeted_amounts, color='blue', label='Budgeted')
#     plt.bar(account_names, actual_amounts, color='green', alpha=0.7, label='Actual')
#     plt.xticks(rotation=45, ha="right")
#     plt.xlabel("Accounts")
#     plt.ylabel("Amount")
#     plt.title("Budget vs. Actual Report")
#     plt.legend()

#     # Save plot to an image
#     buf = io.BytesIO()
#     plt.savefig(buf, format='png')
#     buf.seek(0)
#     string = base64.b64encode(buf.read()).decode('utf-8')
#     buf.close()

#     return f'data:image/png;base64,{string}'
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import matplotlib.pyplot as plt
import io
import urllib, base64
from pesanile_accounting.models import Accounts
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt

@login_required(login_url='/')
def budget_forecast_view(request):
    screen_name = "Budget vs. Actual Report"

    if request.method == 'GET':
        data, total_budget, total_actual, total_forecast_diff = get_budget_forecast_data(company=None)
        chart_url = generate_budget_forecast_chart(data)
        context = {
            'records': data,
            'total_budget': total_budget,
            'total_actual': total_actual,
            'total_forecast_diff': total_forecast_diff,
            'chart_url': chart_url,
            'screen_name': screen_name,
        }
        return render(request, 'reports_acc/budget_forecast.html', context)

def get_budget_forecast_data(company=None):
    """ Fetch accounts with budget and actual balances, and calculate forecast difference. """
    accounts = Accounts.objects.all()
    final_data = []
    total_budget = 0
    total_actual = 0
    total_forecast_diff = 0

    for acc in accounts:
        budgeted_amount = acc.opening_balance
        actual_amount = acc.total_balance
        forecast_difference = actual_amount - budgeted_amount  # Forecast variance

        account_data = {
            'account_name': acc.short_description,
            'budgeted_amount': budgeted_amount,
            'actual_amount': actual_amount,
            'forecast_difference': forecast_difference
        }

        total_budget += budgeted_amount
        total_actual += actual_amount
        total_forecast_diff += forecast_difference
        final_data.append(account_data)

    return final_data, total_budget, total_actual, total_forecast_diff

def generate_budget_forecast_chart(data):
    """ Generate a bar chart comparing actual vs. budgeted amounts and forecast differences. """
    account_names = [d['account_name'] for d in data]
    budgeted_amounts = [d['budgeted_amount'] for d in data]
    actual_amounts = [d['actual_amount'] for d in data]
    forecast_differences = [d['forecast_difference'] for d in data]

    plt.figure(figsize=(10, 5))
    plt.plot(account_names, budgeted_amounts, marker='o', linestyle='-', color='blue', label='Budgeted')
    plt.plot(account_names, actual_amounts, marker='s', linestyle='-', color='green', label='Actual')
    plt.bar(account_names, forecast_differences, color='red', alpha=0.5, label='Forecast Difference')

    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Accounts")
    plt.ylabel("Amount")
    plt.title("Budget vs. Actual with Forecast Difference")
    plt.legend()

    # Save plot to an image
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return f'data:image/png;base64,{string}'

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from pesanile_accounting.models import Accounts, AccountEntry


@login_required(login_url='/')
def receipts_expenditure_view(request):
    """ Statement of Receipts & Expenditures """
    
    total_receipts = Accounts.objects.filter(account_category__name='Bank').aggregate(Sum('total_balance'))['total_balance__sum'] or 0

    total_expenditures = Accounts.objects.filter(account_category__name='Expense').aggregate(Sum('total_balance'))['total_balance__sum'] or 0

    return render(request, 'reports_acc/receipts_expenditure.html', {
        'total_receipts': total_receipts,
        'total_expenditures': total_expenditures
    })


@login_required(login_url='/')
def financial_position_view(request):
    """ Statement of Financial Position """
    assets = Accounts.objects.filter(account_category__name='Other Current Asset').aggregate(Sum('total_balance'))['total_balance__sum'] or 0
    print('assets',assets)
    liabilities = Accounts.objects.filter(account_category__name='Other Current Liability').aggregate(Sum('total_balance'))['total_balance__sum'] or 0
    equity = assets - liabilities
    
    return render(request, 'reports_acc/financial_position.html', {
        'assets': assets, 'liabilities': liabilities, 'equity': equity
    })

@login_required(login_url='/')
def changes_in_equity_view(request):
    """ Statement of Changes in Equity """
    opening_equity = Accounts.objects.filter(account_category__name='Equity').aggregate(Sum('opening_balance'))['opening_balance__sum'] or 0
    current_equity = Accounts.objects.filter(account_category__name='Equity').aggregate(Sum('total_balance'))['total_balance__sum'] or 0
    equity_change = current_equity - opening_equity
    
    return render(request, 'reports_acc/changes_in_equity.html', {
        'opening_equity': opening_equity,
        'current_equity': current_equity,
        'equity_change': equity_change
    })

