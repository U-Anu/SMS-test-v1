from pesanile_accounting.models import *
from django.db.models import Sum
from django.db.models import Q
from django.forms.models import model_to_dict
from datetime import date, datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.utils.timezone import make_aware

from reports.models import Calculationmapping, PL_Calculationmapping, PL_Reportmapping, Reportmapping
from reports.serializers import AccountsSerializer


def trial_balance_report(company_name=None,branch_name=None):
    if company_name is not None and branch_name is not None:
        accounts = Accounts.objects.select_related('gl_line').filter(
            Q(company_name=company_name) and Q(branch_name=branch_name))

    if company_name is None or branch_name is None:
        accounts = Accounts.objects.select_related('gl_line').all().order_by('account_number')

    report_data = []
    total_debit = 0
    total_credit = 0

    for account in accounts:
        entries = AccountEntry.objects.filter(Q(account_number=account))
        print('entries ',entries)
        debit = entries.filter(debit_credit_marker='Debit').aggregate(total=Sum('amount'))['total'] or 0
        credit = entries.filter(debit_credit_marker='Credit').aggregate(total=Sum('amount'))['total'] or 0

        report_data.append({
            'gl_line_number': account.gl_line.gl_line_number if account.gl_line else "-",
            'account_number': account.account_number,
            'description': account.short_description or (account.gl_line.description if account.gl_line else "-"),
            'debit': debit,
            'credit': credit,
        })

        total_debit += debit
        total_credit += credit

    data = {
        'report_data': report_data,
        'total_debit': total_debit,
        'total_credit': total_credit,
    }
    print('data ',data)
    return data

def general_ledger_report(company_name=None,branch_name=None):
    if company_name is not None and branch_name is not None:
        entries = AccountEntry.objects.select_related('account_number__gl_line').filter(Q(company_name=company_name)&Q(branch_name=branch_name)).order_by('entry_date')
    if company_name is not None and branch_name is None:
        entries = AccountEntry.objects.select_related('account_number__gl_line').filter(company_name=company_name).order_by('entry_date')
    if company_name is  None or branch_name is None:
        entries = AccountEntry.objects.select_related('account_number__gl_line').all().order_by('entry_date')

    report_data = []
    running_balance = 0
    total_debit = 0
    total_credit = 0

    for entry in entries:
        debit = entry.amount if entry.debit_credit_marker == 'Debit' else 0
        credit = entry.amount if entry.debit_credit_marker == 'Credit' else 0

        running_balance += (debit - credit)

        report_data.append({
            'date': entry.entry_date.strftime('%Y-%m-%d'),
            'gl_line_number': entry.account_number.gl_line.gl_line_number if entry.account_number.gl_line else '-',
            'account_number': entry.account_number.account_number,
            'description': entry.transaction_code.template_description if entry.transaction_code else '-',
            'debit': debit,
            'credit': credit,
            'running_balance': running_balance,
        })

        total_debit += debit
        total_credit += credit

    data = {
        'report_data': report_data,
        'total_debit': total_debit,
        'total_credit': total_credit,
    }
    return data

def profit_and_loss_statement(company_name=None,branch_name=None):
    # Define GL Line codes for Revenue, COGS, and Expenses
    revenue_gl_lines = ['5001']
    cogs_gl_lines = ['6001-01']
    expenses_gl_lines = ['6200', '6002-01']
    if company_name is not None and branch_name is not None:
        # Calculate Revenue
        revenue_entries = AccountEntry.objects.filter(
            Q(account_number__gl_line__gl_line_number__in=revenue_gl_lines) & (
                        Q(company_name=company_name) and Q(branch_name=branch_name)))
        total_revenue = revenue_entries.aggregate(total=Sum('amount'))['total'] or 0

        # Calculate COGS
        cogs_entries = AccountEntry.objects.filter(Q(account_number__gl_line__gl_line_number__in=cogs_gl_lines) & (
                    Q(company_name=company_name) and Q(branch_name=branch_name)))
        total_cogs = cogs_entries.aggregate(total=Sum('amount'))['total'] or 0

        # Calculate Expenses
        expenses_entries = AccountEntry.objects.filter(
            Q(account_number__gl_line__gl_line_number__in=expenses_gl_lines) & (
                        Q(company_name=company_name) and Q(branch_name=branch_name)))
        total_expenses = expenses_entries.aggregate(total=Sum('amount'))['total'] or 0

    if company_name is not None and branch_name is None:
        # Calculate Revenue
        revenue_entries = AccountEntry.objects.filter(
            Q(account_number__gl_line__gl_line_number__in=revenue_gl_lines) &
                        Q(company_name=company_name))
        total_revenue = revenue_entries.aggregate(total=Sum('amount'))['total'] or 0

        # Calculate COGS
        cogs_entries = AccountEntry.objects.filter(Q(account_number__gl_line__gl_line_number__in=cogs_gl_lines)  &
                        Q(company_name=company_name))
        total_cogs = cogs_entries.aggregate(total=Sum('amount'))['total'] or 0

        # Calculate Expenses
        expenses_entries = AccountEntry.objects.filter(
            Q(account_number__gl_line__gl_line_number__in=expenses_gl_lines)  &
                        Q(company_name=company_name))
        total_expenses = expenses_entries.aggregate(total=Sum('amount'))['total'] or 0

    # Calculate Gross Profit and Net Profit
    gross_profit = total_revenue - total_cogs
    net_profit = gross_profit - total_expenses

    data = {
        'revenue_entries': revenue_entries,
        'total_revenue': total_revenue,
        'cogs_entries': cogs_entries,
        'total_cogs': total_cogs,
        'expenses_entries': expenses_entries,
        'total_expenses': total_expenses,
        'gross_profit': gross_profit,
        'net_profit': net_profit,
    }
    return data

def generate_profit_and_loss_statement(company_name=None,branch_name=None):
    # Filter Account Entries by type 'PL' and date range
    # start_date: datetime, end_date: datetime
    if company_name is not None and branch_name is not None:
        account_entries = AccountEntry.objects.filter(
            Q(entry_type="PL") & (Q(company_name=company_name) & Q(branch_name=branch_name))
        )
        revenue_entries = account_entries.filter(
            Q(debit_credit_marker="Credit") & (Q(company_name=company_name) & Q(branch_name=branch_name)))

    if company_name is not None and branch_name is None:
        account_entries = AccountEntry.objects.filter(Q(entry_type="PL") & Q(company_name=company_name))
        revenue_entries = account_entries.filter(Q(debit_credit_marker="Credit") &Q(company_name=company_name))

    # posting_date__range = [start_date, end_date]
    # Revenue: Sum credits
    total_revenue = revenue_entries.aggregate(total=Sum('amount'))['total'] or 0

    # COGS: Sum debits under relevant GL Line categories
    cogs_entries = account_entries.filter(
        debit_credit_marker="Debit", transaction_code__gl_line__name__icontains="COGS"
    )
    total_cogs = cogs_entries.aggregate(total=Sum('amount'))['total'] or 0

    # Expenses: Sum debits excluding COGS
    expense_entries = account_entries.filter(
        debit_credit_marker="Debit"
    ).exclude(transaction_code__gl_line__name__icontains="COGS")
    total_expenses = expense_entries.aggregate(total=Sum('amount'))['total'] or 0

    # Calculate Gross Profit and Net Profit
    gross_profit = total_revenue - total_cogs
    net_profit = gross_profit - total_expenses

    # Format results for display
    data = {
        "Revenue": {
            "details": revenue_entries.values('transaction_code__gl_line__gl_line_number', 'amount'),
            "total": total_revenue
        },
        "COGS": {
            "details": cogs_entries.values('transaction_code__gl_line__gl_line_number', 'amount'),
            "total": total_cogs
        },
        "Expenses": {
            "details": expense_entries.values('transaction_code__gl_line__gl_line_number', 'amount'),
            "total": total_expenses
        },
        "Gross Profit": gross_profit,
        "Net Profit": net_profit
    }

    return data

# def generate_cash_flow_statement(company_name=None,branch_name=None):
#     # Fetch all account entries
#     if company_name is not None and branch_name is not None:
#         entries = AccountEntry.objects.filter(Q(company_name=company_name) & Q(branch_name=branch_name)
#         )
#     if company_name is not None and branch_name is None:
#         entries = AccountEntry.objects.filter(company_name=company_name)

#     if company_name is  None or branch_name is None:
#         entries = AccountEntry.objects.all()

#     # Operating Activities
#     cash_from_sales = (
#         entries.filter(account_number__gl_line__gl_line_number='1001-01')
#         .aggregate(total=Sum('amount'))['total'] or 0
#     )
#     salaries_paid = (
#         entries.filter(account_number__gl_line__gl_line_number='6002-01')
#         .aggregate(total=Sum('amount'))['total'] or 0
#     )
#     net_operating_cash_flow = cash_from_sales - abs(salaries_paid)

#     # Investing Activities
#     stock_purchase = (
#         entries.filter(account_number__gl_line__gl_line_number='1002-01')
#         .aggregate(total=Sum('amount'))['total'] or 0
#     )
#     net_investing_cash_flow = -abs(stock_purchase)

#     # Financing Activities
#     cash_deposited_to_bank = (
#         entries.filter(account_number__gl_line__gl_line_number='1001-02')
#         .aggregate(total=Sum('amount'))['total'] or 0
#     )
#     net_financing_cash_flow = -abs(cash_deposited_to_bank)

#     # Net Cash Flow
#     net_cash_flow = net_operating_cash_flow + net_investing_cash_flow + net_financing_cash_flow

#     # Cash Flow Statement
#     cash_flow_statement = {
#         'Operating Activities': {
#             'Cash from Sales': cash_from_sales,
#             'Salaries Paid': -abs(salaries_paid),
#             'Net Operating Cash Flow': net_operating_cash_flow,
#         },
#         'Investing Activities': {
#             'Stock Purchase': -abs(stock_purchase),
#             'Net Investing Cash Flow': net_investing_cash_flow,
#         },
#         'Financing Activities': {
#             'Cash Deposited to Bank': -abs(cash_deposited_to_bank),
#             'Net Financing Cash Flow': net_financing_cash_flow,
#         },
#         'Net Cash Flow': net_cash_flow,
#     }

#     return cash_flow_statement

from django.db.models import Q, Sum

def generate_cash_flow_statement(company_name=None, branch_name=None):
    # Fetch all account entries based on filters
    if company_name and branch_name:
        entries = AccountEntry.objects.filter(Q(company_name=company_name) & Q(branch_name=branch_name))
    elif company_name:
        entries = AccountEntry.objects.filter(company_name=company_name)
    else:
        entries = AccountEntry.objects.all()

    # Map GL line numbers dynamically
    gl_mapping = {
        "Cash from Sales": ["1000"],
        "Salaries Paid": ["2400"],
        "Stock Purchase": ["1210"],
        "Cash Deposited to Bank": ["10051", "1100"],
    }

    # Operating Activities
    cash_from_sales = (
        entries.filter(account_number__gl_line__gl_line_number__in=gl_mapping["Cash from Sales"])
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    salaries_paid = (
        entries.filter(account_number__gl_line__gl_line_number__in=gl_mapping["Salaries Paid"])
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    net_operating_cash_flow = cash_from_sales - abs(salaries_paid)

    # Investing Activities
    stock_purchase = (
        entries.filter(account_number__gl_line__gl_line_number__in=gl_mapping["Stock Purchase"])
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    net_investing_cash_flow = -abs(stock_purchase)

    # Financing Activities
    cash_deposited_to_bank = (
        entries.filter(account_number__gl_line__gl_line_number__in=gl_mapping["Cash Deposited to Bank"])
        .aggregate(total=Sum("amount"))["total"] or 0
    )
    net_financing_cash_flow = -abs(cash_deposited_to_bank)

    # Net Cash Flow
    net_cash_flow = net_operating_cash_flow + net_investing_cash_flow + net_financing_cash_flow

    # Cash Flow Statement
    cash_flow_statement = {
        "Operating Activities": {
            "Cash from Sales": cash_from_sales,
            "Salaries Paid": -abs(salaries_paid),
            "Net Operating Cash Flow": net_operating_cash_flow,
        },
        "Investing Activities": {
            "Stock Purchase": -abs(stock_purchase),
            "Net Investing Cash Flow": net_investing_cash_flow,
        },
        "Financing Activities": {
            "Cash Deposited to Bank": -abs(cash_deposited_to_bank),
            "Net Financing Cash Flow": net_financing_cash_flow,
        },
        "Net Cash Flow": net_cash_flow,
    }

    return cash_flow_statement

def generate_balance_sheet(company_name=None,branch_name=None):
    # Current Assets
    current_assets = Accounts.objects.filter(
        gl_line__asset_type__name='Current Assets'
    ).aggregate(total_balance=Sum('total_balance'))['total_balance'] or 0

    # Non-Current Assets
    non_current_assets = Accounts.objects.filter(
        gl_line__asset_type__name='Non-Current Assets'
    ).aggregate(total_balance=Sum('total_balance'))['total_balance'] or 0

    # Liabilities
    total_liabilities = Accounts.objects.filter(
        gl_line__asset_type__name='Liabilities'
    ).aggregate(total_balance=Sum('total_balance'))['total_balance'] or 0

    # Equity
    total_equity = Accounts.objects.filter(
        gl_line__asset_type__name='Equity'
    ).aggregate(total_balance=Sum('total_balance'))['total_balance'] or 0

    # Total Assets
    total_assets = current_assets + non_current_assets

    # Check the Balance
    balance_sheet = {
        'Current Assets': current_assets,
        'Non-Current Assets': non_current_assets,
        'Total Assets': total_assets,
        'Liabilities': total_liabilities,
        'Equity': total_equity,
        'Assets - (Liabilities + Equity)': total_assets - (total_liabilities + total_equity),
    }

    return balance_sheet

def profit_and_loss(company_name=None,branch_name=None):
    sales_glline , food_glline, salary_glline = '1003', '1034', '1025'
    sales_rev = GLLine.objects.get(gl_line_number='1003')
    food_cost = GLLine.objects.get(gl_line_number='1034')
    # partner_commission = GLLine.objects.get(gl_line_number='6200')
    salary = GLLine.objects.get(gl_line_number='1025')
    glline_id = [sales_rev.pk,food_cost.pk,salary.pk]
    name = ['Sales Revenue','Food Costs','Salaries']
    glline = [sales_glline,food_glline,salary_glline]
    response_data = []
    for ids, name, glline in zip(glline_id,name,glline):
        acc = Accounts.objects.filter(gl_line=ids).first()
        data = {
            'description' : name,
            'glline' : glline,
            'amount' : acc.total_balance if acc is not None else 0,
        }
        response_data.append(data)
    return response_data

def account_payable_aging(company_name=None,branch_name=None):
    if company_name is None or branch_name is None:
        obj=AccountPayable.objects.all()
    else:
        obj = AccountPayable.objects.filter(Q(company_name=company_name)|Q(branch_name=branch_name))
    response_data = []
    for data in obj:
        my_dict = {
            'vendor_id': data.vendor_id,
            'glline_code': '3001',
            'reference_type': data.reference_type,
            'reference_no': data.reference_number,
            'invoice_date': data.effective_from,
            'amount': data.actual_amount,
        }
        response_data.append(my_dict)


    return response_data

def account_receivable_aging(company_name=None,branch_name=None):
    if company_name is None or branch_name is None:
        obj=AccountReceivable.objects.all()
    else:
        obj = AccountReceivable.objects.filter(Q(company_name=company_name)|Q(branch_name=branch_name))
    response_data = []
    for data in obj:
        my_dict = {
            'customer_id': data.student_id,
            'glline_code': '1200',
            'reference_type': data.reference_type,
            'reference_no': data.reference_number,
            'invoice_date': data.effective_from,
            'amount': data.actual_amount,
        }
        response_data.append(my_dict)
    return response_data

from collections import defaultdict
def balance_sheet(company_name=None,branch_name=None):
    asset_type_obj = AssetType.objects.all().order_by('created_at')
    response_data = []
    for ato in asset_type_obj:
        glline_obj = GLLine.objects.filter(asset_type=ato)
        for glo in glline_obj:
            if company_name is not None and branch_name is not None:
                acc_obj = Accounts.objects.filter(Q(gl_line=glo) & (Q(company_name=company_name) & Q(branch_name=branch_name)))
            if company_name is not None and branch_name is None:
                acc_obj = Accounts.objects.filter(Q(gl_line=glo) & Q(company_name=company_name))

            amount = acc_obj.aggregate(Sum('total_balance')).get('total_balance__sum')
            data = {
                'main_header': ato.name,
                'name': glo.name,
                'glline': glo.gl_line_number,
                'amount': 0.0 if amount is None else amount
            }
            response_data.append(data)
    return response_data

def petty_cash(company_name=None,branch_name=None):
    glline_obj = GLLine.objects.get(gl_line_number='1047')
    response_data = []
    acc_obj = Accounts.objects.filter(gl_line=glline_obj)
    if company_name is not None and branch_name is not None:
        acc_obj = Accounts.objects.filter(Q(gl_line=glline_obj) & (Q(company_name=company_name) & Q(branch_name=branch_name)))

    if company_name is not None and branch_name is None:
        acc_obj = Accounts.objects.filter(Q(gl_line=glline_obj) & Q(company_name=company_name))

    for acc in acc_obj:
        if company_name is not None and branch_name is not None:
            dr_acc_entry_obj = AccountEntry.objects.filter((Q(account_number=acc) & Q(debit_credit_marker='Debit')) & (
                        Q(company_name=company_name) and Q(branch_name=branch_name)))
            cr_acc_entry_obj = AccountEntry.objects.filter((Q(account_number=acc) & Q(debit_credit_marker='Credit')) & (
                        Q(company_name=company_name) and Q(branch_name=branch_name)))

        if company_name is not None and branch_name is None:
            dr_acc_entry_obj = AccountEntry.objects.filter((Q(account_number=acc) & Q(debit_credit_marker='Debit')) &
                    Q(company_name=company_name))
            cr_acc_entry_obj = AccountEntry.objects.filter((Q(account_number=acc) & Q(debit_credit_marker='Credit')) &
                               Q(company_name=company_name))

        data_dict = {
            'date' : acc.updated_at,
            'glline_code' : glline_obj.pk,
            'account_number' : acc.account_number,
            'debit' : 0.0 if dr_acc_entry_obj.aggregate(Sum('amount')).get('amount__sum') is None else dr_acc_entry_obj.aggregate(Sum('amount')).get('amount__sum'),
            'credit' : 0.0 if cr_acc_entry_obj.aggregate(Sum('amount')).get('amount__sum') is None else cr_acc_entry_obj.aggregate(Sum('amount')).get('amount__sum'),
            'balance' : acc.total_balance
        }
        response_data.append(data_dict)
    return response_data

def trial_balance_by_period(company_name=None,branch_name=None):
    # Calculate periods dynamically from the start of the year to the current month
    start_date = date(date.today().year, 1, 1)
    end_date = date.today()

    # Convert naive dates to timezone-aware dates
    start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
    end_date = timezone.make_aware(datetime.combine(end_date, datetime.min.time()))

    # Generate a list of months from January to the current month
    periods = []
    current_date = start_date
    while current_date <= end_date:
        period_start = current_date.replace(day=1)
        period_end = (current_date + relativedelta(months=1) - relativedelta(days=1))

        # Make period dates timezone-aware
        period_start = timezone.make_aware(datetime.combine(period_start, datetime.min.time()))
        period_end = timezone.make_aware(datetime.combine(period_end, datetime.min.time()))

        periods.append({
            'start': period_start,
            'end': period_end,
            'label': current_date.strftime('%B')  # e.g., "January (USD)"
        })
        current_date += relativedelta(months=1)

    # Fetch GL lines
    gl_lines = GLLine.objects.all()

    # Prepare report data
    report_data = []
    for gl_line in gl_lines:
        row = {
            'gl_code': gl_line.gl_line_number,
            'account_name': gl_line.name,
        }
        for period in periods:
            # Calculate the balance for the period
            if company_name is not None and branch_name is not None:
                balance_debit = AccountEntry.objects.filter(
                    Q(account_number__gl_line=gl_line,
                      entry_date__range=[period['start'], period['end']],
                      debit_credit_marker='Debit') & (Q(company_name=company_name) & Q(branch_name=branch_name))
                ).aggregate(Sum('amount'))
                balance_credit = AccountEntry.objects.filter(
                    Q(account_number__gl_line=gl_line,
                      entry_date__range=[period['start'], period['end']],
                      debit_credit_marker='Credit') & (Q(company_name=company_name) & Q(branch_name=branch_name))
                ).aggregate(Sum('amount'))
            if company_name is None or branch_name is None:
                balance_debit = AccountEntry.objects.filter(
                    Q(account_number__gl_line=gl_line,
                      entry_date__range=[period['start'], period['end']],
                      debit_credit_marker='Debit')).aggregate(Sum('amount'))
                balance_credit = AccountEntry.objects.filter(
                    Q(account_number__gl_line=gl_line,
                      entry_date__range=[period['start'], period['end']],
                      debit_credit_marker='Credit')).aggregate(Sum('amount'))
            if company_name is not None and branch_name is None:
                balance_debit = AccountEntry.objects.filter(
                    Q(account_number__gl_line=gl_line,
                      entry_date__range=[period['start'], period['end']],
                      debit_credit_marker='Debit') & Q(company_name=company_name)
                ).aggregate(Sum('amount'))
                balance_credit = AccountEntry.objects.filter(
                    Q(account_number__gl_line=gl_line,
                      entry_date__range=[period['start'], period['end']],
                      debit_credit_marker='Credit') & Q(company_name=company_name)
                ).aggregate(Sum('amount'))
            net_balance = (balance_debit.get('amount__sum') or 0) - (balance_credit.get('amount__sum') or 0)
            row[period['label']] = net_balance

        report_data.append(row)
    return report_data


def cash_book_detailed_report_all(company_name=None,branch_name=None, is_superuser=False):
    # Get all GL lines for cash accounts (assuming they are named with "Cash")
    cash_gl_lines = GLLine.objects.filter(name__icontains="Cash")
    if not cash_gl_lines.exists():
        return {"error": "No Cash GL Lines found. Please verify your GL setup."}

    # Fetch all transactions associated with cash accounts
    if company_name is not None and branch_name is not None:
        print('here.....1')
        transactions = AccountEntry.objects.filter(
            Q(account_number__gl_line__in=cash_gl_lines)&(Q(company_name=company_name)|Q(branch_name=branch_name))
        ).order_by("entry_date")
        # Prepare the opening balance for all cash GL lines
        opening_balance = AccountEntry.objects.filter(Q(
            account_number__gl_line__in=cash_gl_lines,
            entry_date__lt=transactions.first().entry_date if transactions.exists() else None) & Q(
            company_name=company_name)).aggregate(
            receipts=Sum('amount', filter=Q(debit_credit_marker="Debit")&(Q(company_name=company_name) & Q(branch_name=branch_name))),
            payments=Sum('amount', filter=Q(debit_credit_marker="Credit")&(Q(company_name=company_name)& Q(branch_name=branch_name)))
        )
    if company_name is None or branch_name is None:
        print('here.....1')
        transactions = AccountEntry.objects.filter(
            Q(account_number__gl_line__in=cash_gl_lines)).order_by("entry_date")
        # Prepare the opening balance for all cash GL lines
        opening_balance = AccountEntry.objects.filter(Q(
            account_number__gl_line__in=cash_gl_lines,
            entry_date__lt=transactions.first().entry_date if transactions.exists() else None)).aggregate(
            receipts=Sum('amount', filter=Q(debit_credit_marker="Debit")),
            payments=Sum('amount', filter=Q(debit_credit_marker="Credit"))
        )
    if company_name is not None and branch_name is None:
        print('here.....2')
        transactions = AccountEntry.objects.filter(
            Q(account_number__gl_line__in=cash_gl_lines)&(Q(company_name=company_name)|Q(branch_name=branch_name))
        ).order_by("entry_date")
        # Prepare the opening balance for all cash GL lines
        opening_balance = AccountEntry.objects.filter(Q(
            account_number__gl_line__in=cash_gl_lines,
            entry_date__lt=transactions.first().entry_date if transactions.exists() else None) & Q(
            company_name=company_name)).aggregate(
            receipts=Sum('amount', filter=(Q(debit_credit_marker="Debit")&Q(company_name=company_name))),
            payments=Sum('amount', filter=(Q(debit_credit_marker="Credit")&Q(company_name=company_name)))
        )
    if is_superuser:
        transactions = AccountEntry.objects.filter(account_number__gl_line__in=cash_gl_lines).order_by("entry_date")
        # Prepare the opening balance for all cash GL lines
        opening_balance = AccountEntry.objects.filter(
            account_number__gl_line__in=cash_gl_lines,
            entry_date__lt=transactions.first().entry_date if transactions.exists() else None).aggregate(
            receipts=Sum('amount', filter=Q(debit_credit_marker="Debit"),
            payments=Sum('amount', filter=Q(debit_credit_marker="Credit")),
        ))



    opening_balance = (opening_balance.get('receipts') or 0) - (opening_balance.get('payments') or 0)

    # Prepare the report data
    report_data = []
    current_balance = opening_balance

    # Add opening balance row
    report_data.append({
        "date": "Opening Balance",
        "description": "Opening Balance",
        "receipts": "",
        "payments": "",
        "balance": current_balance,
    })

    # Process each transaction
    for txn in transactions:
        if txn.debit_credit_marker == "Debit":  # Receipt
            receipt = txn.amount
            payment = ""
            current_balance += txn.amount
        elif txn.debit_credit_marker == "Credit":  # Payment
            receipt = ""
            payment = txn.amount
            current_balance -= txn.amount
        else:
            receipt = payment = ""

        report_data.append({
            "date": txn.entry_date.strftime("%Y-%m-%d"),
            "description": txn.account_number.short_description,
            "receipts": receipt,
            "payments": payment,
            "balance": current_balance,
        })

    return report_data


def accounts_payable_vs_receivable_summary(company_name=None,branch_name=None):
    if company_name is None or branch_name is None:
        receivables_total = AccountEntry.objects.filter(
        Q(account_number__account_type__name__icontains="Receivable",
        debit_credit_marker="Debit")).aggregate(total=Sum("amount"))["total"] or 0

    # Query accounts marked for payables
        payables_total = AccountEntry.objects.filter(
        Q(account_number__account_type__name__icontains="Payable",
        debit_credit_marker="Credit")).aggregate(total=Sum("amount"))["total"] or 0
    
    else:
    # Query accounts marked for receivables
        receivables_total = AccountEntry.objects.filter(
            Q(account_number__account_type__name__icontains="Receivable",
            debit_credit_marker="Debit")&(Q(company_name=company_name)|Q(branch_name=branch_name))
        ).aggregate(total=Sum("amount"))["total"] or 0

        # Query accounts marked for payables
        payables_total = AccountEntry.objects.filter(
            Q(account_number__account_type__name__icontains="Payable",
            debit_credit_marker="Credit")&(Q(company_name=company_name)|Q(branch_name=branch_name))
        ).aggregate(total=Sum("amount"))["total"] or 0

    # Calculate net position
    net_position = receivables_total - payables_total

    # Prepare the summary
    summary = [
        {"category": "Total Receivables", "amount": receivables_total},
        {"category": "Total Payables", "amount": payables_total},
        {"category": "Net Position", "amount": net_position},
    ]

    return summary

def petty_cash_usage_report(company_name=None,branch_name=None):
    # Get the petty cash GL line
    glline_obj = GLLine.objects.get(gl_line_number='1047')

    # Fetch all accounts under the petty cash GL line
    accounts = Accounts.objects.filter(Q(gl_line=glline_obj)&(Q(company_name=company_name)|Q(branch_name=branch_name)))

    # Fetch all transactions for these accounts
    transactions = AccountEntry.objects.filter(Q(account_number__in=accounts)&(Q(company_name=company_name)|Q(branch_name=branch_name))).order_by("entry_date")

    # Initialize the response and calculate the opening balance
    response_data = []
    running_balance = sum(
        accounts.filter(account_type="Petty Cash").values_list("total_balance", flat=True)
    )

    for txn in transactions:
        if txn.debit_credit_marker == "Credit":
            running_balance -= txn.amount
        else:
            running_balance += txn.amount

        response_data.append({
            "date": txn.entry_date,
            # "purpose": txn.description,
            "amount": txn.amount,
            "balance": running_balance,
        })

    return response_data

def journal_summary_report(start_date=None, end_date=None,company_name=None,branch_name=None):
    """
    Generate a summary of journal entries from the AccountEntry table.

    :param start_date: Start date for the report (inclusive).
    :param end_date: End date for the report (inclusive).
    :return: List of journal summary data.
    """
    # Filter AccountEntry objects by date range if provided
    if company_name is None or branch_name is None:
        account_entries = AccountEntry.objects.all()
    else:
        account_entries = AccountEntry.objects.filter(Q(company_name=company_name)|Q(branch_name=branch_name))
    if start_date and end_date:
        account_entries = account_entries.filter(entry_date__range=[start_date, end_date])

    # Group data by a unique transaction description or identifier
    grouped_entries = account_entries.values("entry_date","account_number").annotate(
        total_debit=Sum("amount", filter=Q(debit_credit_marker="Debit")),
        total_credit=Sum("amount", filter=Q(debit_credit_marker="Credit"))
    )
    print('grouped_entries ',grouped_entries)

    # Prepare the report data
    report_data = []
    for entry in grouped_entries:
        report_data.append({
            # "description": entry["description"],
            "date": entry["entry_date"],
            "account_number": entry["account_number"],
            "debit": entry["total_debit"] or 0.0,
            "credit": entry["total_credit"] or 0.0,
        })

    return report_data




from django.utils.dateparse import parse_date

def get_total(final_value):
    cal_mapping=Calculationmapping.objects.filter(report_type__name='Balance sheet')
    total_final_list=[]
    for cur_cat in cal_mapping:
        dict = {}
        name_list=[]
        added_total=0
        cal_obj=cur_cat.assect_catogery.all()
        print("cal_obj",cal_obj)
        for i in cal_obj:
            name_list.append(i.name)
            print("name",i.name)
            # m=final_value[f'{i.name}']['overall_cat_total']
            # print("totyal",m)
            for data in final_value:
                if data['catogory_id'] == i.asset_type_category_id:
                    added_total += data['overall_cat_total']
        # dict['name']=name_list.join(',','&')
        if len(name_list) > 1:
            dict['name'] = ', '.join(name_list[:-1]) + ' & ' + name_list[-1]
        else:
            dict['name'] = name_list[0] if name_list else ''

        dict['total']=added_total
        total_final_list.append(dict)
    print("total_final_list",total_final_list)  
        
    return total_final_list
def get_accentry(acc_obj,from_date,to_date,year_selection):
    if year_selection == "current_year":
            from_date = str(date(datetime.today().year, 1, 1))  # January 1st of current year
            to_date = str(date(datetime.today().year, 12, 31))  # December 31st of current year
            print("current_year from_date",from_date,type(from_date))
            print("current_year to_date",to_date, type(to_date))

    elif year_selection == "previous_year":
            prev_year = datetime.today().year - 1
            from_date = str( date(prev_year, 1, 1))  # January 1st of previous year
            to_date = str(date(prev_year, 12, 31))  # December 31st of previous year
            print("previous_year from_date",from_date)
            print("previous_year to_date",to_date)
    if from_date:
            print("for convert from_date",from_date)
            from_date = parse_date(from_date)
    if to_date:
            print("for convert to_date",to_date)
            to_date = parse_date(to_date)
    print("from_date",from_date)
    print("to_date",to_date)
    total_amount_final = 0
    my_list = []
    for i in acc_obj:
        print("account number",i.account_number)
        print("account short_description",i.short_description)
        
        accentry_obj=AccountEntry.objects.filter(Q(account_number__account_number=i.account_number)&Q(entry_date__date__range=[from_date, to_date]))
        print("accentry_obj=====>",accentry_obj)
        debit = accentry_obj.filter(debit_credit_marker='Debit').aggregate(total=Sum('amount'))['total'] or 0
        credit = accentry_obj.filter(debit_credit_marker='Credit').aggregate(total=Sum('amount'))['total'] or 0
        total_amount=debit+credit
        total_amount_final = total_amount_final+total_amount
        my_dict = {
            'account_number':i.account_number,
            'short_description':i.short_description,
            'total_balance' : total_amount,
        }
        print('my_dict ',my_dict)
        my_list.append(my_dict)
        print("amount for this account",i.account_number,'-',total_amount)
    
    print('my_list ',my_list)
    return [my_list,total_amount_final]

def balance_sheet_new_new(company_name=None, branch_name=None,from_date=None,to_date=None,year_selection=None):
    final_value=[]
    
    report_mapping=Reportmapping.objects.filter(report_type__name='Balance sheet',)
    report_mapping_catogory = list(report_mapping.values_list('asset_catogery_id', flat=True).distinct())
    for cat in report_mapping_catogory:
        value_catogory={}
        catagory_group=report_mapping.filter(asset_catogery=cat)
        # print("catagory_group",catagory_group.assect_type.name)
        data_list=[]
        overall_total=0
        for curr_group in catagory_group:
            value_catogory['Catogory']=curr_group.asset_catogery.name
            value_catogory['catogory_id']=curr_group.asset_catogery.asset_type_category_id
            gl_dict={}
            gl_dict['gl_name']=f'{curr_group.glline.gl_line_number}-{curr_group.glline.name}'
            print("assect_type",curr_group.asset_type.name)
            
            acc_obj = Accounts.objects.filter(gl_line=curr_group.glline).order_by("account_number")
            for i in acc_obj:
                print("account",i)
                
            if from_date or year_selection :
                print("enter for calling")
                callfun=get_accentry(acc_obj,from_date,to_date,year_selection)
                    
                print("callfuncallfun",callfun)
                accounts = callfun[0]
                amount=callfun[1]
                  
            else:
                amount = acc_obj.aggregate(Sum('total_balance')).get('total_balance__sum') or 0.0
                print("amount in else",amount)
                accounts=AccountsSerializer(acc_obj,many=True).data
            gl_dict['accounts']=accounts
            
            # amount = acc_obj.aggregate(Sum('total_balance')).get('total_balance__sum') or 0.0
            gl_dict['gl_total']=amount
            print('amountamount',amount)
            data_list.append(gl_dict)
            overall_total+=amount
            print("overall_total",overall_total)
            
        value_catogory['account_list']=data_list
        value_catogory['overall_cat_total']=overall_total
        
        print('data_list',data_list)
        print("overall_total",overall_total)
        final_value.append(value_catogory)
        



        
        
    
    print('final_value-----------------',final_value)
    a=get_total(final_value)
    return final_value,a
            
            


def get_totals(final_value):
    cal_mapping=PL_Calculationmapping.objects.filter(report_type__name='P&L')
    total_final_list=[]
    for cur_cat in cal_mapping:
        dict = {}
        added_total=0
        cal_obj=cur_cat.assect_catogery.all()
        print("cal_obj",cal_obj)
        for i in cal_obj:
            print("name",i.name)
            for data in final_value:
                if data['catogory_id'] == i.id:
                    added_total += data['overall_cat_total']
        
        dict['position']=cur_cat.output_positions.id
        dict['name']=cur_cat.name
        dict['total']=added_total
        total_final_list.append(dict)
    print("total_final_list",total_final_list)  
        
    return total_final_list

def profit_and_loss_new_new(company_name=None, branch_name=None):
    final_value=[]
    
    report_mapping=PL_Reportmapping.objects.filter(report_type__name='P&L',)
    report_mapping_catogory = list(report_mapping.values_list('asset_catogery_id', flat=True).distinct())
    for cat in report_mapping_catogory:
        value_catogory={}
        catagory_group=report_mapping.filter(asset_catogery=cat)
        # print("catagory_group",catagory_group.assect_type.name)
        data_list=[]
        overall_total=0
        for curr_group in catagory_group:
            value_catogory['Catogory']=curr_group.asset_catogery.name
            value_catogory['catogory_id']=curr_group.asset_catogery.id
            # value_catogory['catogory_id']=curr_group.asset_catogery.id
            gl_dict={}
            gl_dict['gl_name']=f'{curr_group.glline.gl_line_number}-{curr_group.glline.name}'
            print("asset_catogery",curr_group.asset_catogery.name)
            
            acc_obj = Accounts.objects.filter(gl_line=curr_group.glline).order_by("account_number")
            for i in acc_obj:
                print("account",i)
            gl_dict['accounts']=acc_obj
            amount = acc_obj.aggregate(Sum('total_balance')).get('total_balance__sum') or 0.0
            overall_total+=amount
            gl_dict['gl_total']=amount
            print('amountamount',amount)
            data_list.append(gl_dict)
            print("overall_total",overall_total)
            print("amount in else",amount)
            print("overall_total",overall_total)

        value_catogory['account_list']=data_list
        value_catogory['overall_cat_total']=overall_total
        
        print('data_list',data_list)
        print("overall_total",overall_total)
        final_value.append(value_catogory)
    print('final_value-----------------',final_value)
    a=get_totals(final_value)
    

    return final_value,a


