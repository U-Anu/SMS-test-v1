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
@login_required(login_url='/')
def trail_balance_report_views(request):
    if request.method == 'GET':
        data = trial_balance_report(company_name=request.user.company,branch_name=request.user.branch)
        print('data==========',data)
        template_name = 'reports_acc/trail_balance_report.html'
        return render(request, template_name, data)

# Create your views here.
@login_required(login_url='/')
def general_ledger_report_views(request):
    if request.method == 'GET':
        data = general_ledger_report(company_name=request.user.company,branch_name=request.user.branch)
        template_name = 'reports_acc/general_ledger_report.html'
        return render(request, template_name, data)

# Create your views here.
@login_required(login_url='/')
def generate_cash_flow_statement_views(request):
    screen_name = 'Cash flow statement'
    if request.method == 'GET':
        data = generate_cash_flow_statement(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'cash_flow_statement':data,
            'screen_name':screen_name,
        }
        template_name = 'reports_acc/generate_cash_flow_statement.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def balance_sheet_views(request):
    screen_name = 'Balance sheet'
    if request.method == 'GET':
        data = balance_sheet(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/balance_sheet.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def balance_sheet_views_new(request):
    screen_name = 'Balance sheet'
    if request.method == 'POST':
        from_date=request.POST.get("from_date")
        to_date=request.POST.get("to_date")
        year_selection=request.POST.get("year_selection")
        print("from_date",from_date,'to_date',to_date,'year_selection',year_selection)
        data,cal_total = balance_sheet_new_new(company_name=request.user.company,branch_name=request.user.branch,from_date=from_date,to_date=to_date,year_selection=year_selection)
        context = {
            'records':data,
            'cal_total':cal_total,
            'screen_name':screen_name,
        }    
    if request.method == 'GET':
        data,cal_total= balance_sheet_new_new(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'first':'first',
            'cal_total':cal_total,
            'screen_name':screen_name,
        }    
    template_name = 'reports_acc/balance_sheet_new_final.html'
    return render(request, template_name, context)



# @login_required(login_url='/')
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

@login_required(login_url='/')
def profit_and_loss_statement_views(request):
    screen_name = 'Profit and loss statement'
    if request.method == 'GET':
        data = profit_and_loss(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/profit_and_loss_statement.html'
        return render(request, template_name, context)

from collections import defaultdict

@login_required(login_url='/')
def profit_and_loss_statement_views_new(request):
    screen_name = 'Profit and Loss Statement'
    
    if request.method == 'GET':
        data,cal_total = profit_and_loss_new_new(company_name=request.user.company, branch_name=request.user.branch)
       
        
        
        context = {
            'records': data,
            'cal_total': cal_total,
            'screen_name': screen_name,
        }
        # print('context', context)  # Debugging output
        template_name = 'reports_acc/profit_and_loss_statement_work.html'
        return render(request, template_name, context)


@login_required(login_url='/')
def account_payable_aging_views(request):
    screen_name = 'Account payable aging'
    if request.method == 'GET':
        data = account_payable_aging(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/account_payable_aging.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def account_receivable_aging_views(request):
    screen_name = 'Account receivable aging'
    if request.method == 'GET':
        data = account_receivable_aging(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/account_receivable_aging.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def petty_cash_views(request):
    screen_name = 'Petty cash'
    if request.method == 'GET':
        data = petty_cash(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/petty_cash.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def trial_balance_by_period_views(request):
    screen_name = 'Trial balance by period'
    if request.method == 'GET':
        data = trial_balance_by_period(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/trial_balance_by_period.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def cash_book_detailed_report_all_views(request):
    screen_name = 'Cash book detailed report'
    if request.method == 'GET':
        data = cash_book_detailed_report_all(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/cash_book_detailed_report_all.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def accounts_payable_vs_receivable_summary_views(request):
    screen_name = 'Account payable vs receivable summary'
    if request.method == 'GET':
        data = accounts_payable_vs_receivable_summary(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/accounts_payable_vs_receivable_summary.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def petty_cash_usage_report_views(request):
    screen_name = 'Petty cash usage report'
    if request.method == 'GET':
        data = petty_cash_usage_report(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/petty_cash_usage_report.html'
        return render(request, template_name, context)

@login_required(login_url='/')
def journal_summary_report_views(request):
    screen_name = 'Journal summary report'
    if request.method == 'GET':
        data = journal_summary_report(company_name=request.user.company,branch_name=request.user.branch)
        context = {
            'records':data,
            'screen_name':screen_name,
        }
        print('context',context)
        template_name = 'reports_acc/journal_summary_report_views.html'
        return render(request, template_name, context)

