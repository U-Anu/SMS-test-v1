from django.urls import path
from .views_ram import *
urlpatterns = [
    path('trial-balance-report1/', trail_balance_report_views, name='trail_balance_report1'),
    path('general-ledger-report1/', general_ledger_report_views, name='general_ledger_report1'),
    path('cash-flow-statement1/', generate_cash_flow_statement_views, name='generate_cash_flow_statement_views1'),
    path('balance-sheet1/', balance_sheet_views, name='balance_sheet_views1'),
    path('profit-and-loss-statement1/', profit_and_loss_statement_views, name='profit_and_loss_statement_views1'),
    path('account-payable-aging1/', account_payable_aging_views, name='account_payable_aging_views1'),
    path('account-receivable-aging1/', account_receivable_aging_views, name='account_receivable_aging_views1'),
    path('petty-cash1/', petty_cash_views, name='petty_cash_views1'),
    path('trial-balance-by-period1/', trial_balance_by_period_views, name='trial_balance_by_period_views1'),
    path('cash-book-detailed-report1/', cash_book_detailed_report_all_views, name='cash_book_detailed_report_all_views1'),
    path('accounts-payable-vs-receivable-summary1/', accounts_payable_vs_receivable_summary_views, name='accounts_payable_vs_receivable_summary_views1'),
    path('petty-cash-usage-report1/', petty_cash_usage_report_views, name='petty_cash_usage_report_views1'),
    path('journal-summary-report1/', journal_summary_report_views, name='journal_summary_report_views1'),
    path('profit-and-loss-statement-new/', profit_and_loss_statement_views_new, name='profit_and_loss_statement_views_new'),
    path('balance-sheet-new/', balance_sheet_views_new, name='balance_sheet_views_new'),

    path('budget-forecast1/', budget_forecast_view, name='budget_forecast_views1'),
    path('receipts-expenditure/', receipts_expenditure_view, name='receipts_expenditure'),
    path('financial-position/', financial_position_view, name='financial_position'),
    path('changes-in-equity/', changes_in_equity_view, name='changes_in_equity'),
    # path('profit-and-loss-statement/', profit_and_loss_statement_views, name='profit_and_loss_statement_views'),
]