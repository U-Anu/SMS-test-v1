from django.urls import path
from .views_ram import *
urlpatterns = [
    path('trial-balance-report/', trail_balance_report_views, name='trail_balance_report'),
    path('general-ledger-report/', general_ledger_report_views, name='general_ledger_report'),
    path('cash-flow-statement/', generate_cash_flow_statement_views, name='generate_cash_flow_statement_views'),
    path('balance-sheet/', balance_sheet_views, name='balance_sheet_views'),
    path('balance-sheet-new/', balance_sheet_views_new, name='balance_sheet_views_new'),
    path('profit-and-loss-statement/', profit_and_loss_statement_views, name='profit_and_loss_statement_views'),
    path('profit-and-loss-statement-new/', profit_and_loss_statement_views_new, name='profit_and_loss_statement_views_new'),
    path('account-payable-aging/', account_payable_aging_views, name='account_payable_aging_views'),
    path('account-receivable-aging/', account_receivable_aging_views, name='account_receivable_aging_views'),
    path('petty-cash/', petty_cash_views, name='petty_cash_views'),
    path('trial-balance-by-period/', trial_balance_by_period_views, name='trial_balance_by_period_views'),
    path('cash-book-detailed-report/', cash_book_detailed_report_all_views, name='cash_book_detailed_report_all_views'),
    path('accounts-payable-vs-receivable-summary/', accounts_payable_vs_receivable_summary_views, name='accounts_payable_vs_receivable_summary_views'),
    path('petty-cash-usage-report/', petty_cash_usage_report_views, name='petty_cash_usage_report_views'),
    path('journal-summary-report/', journal_summary_report_views, name='journal_summary_report_views'),
    
    # path('profit-and-loss-statement/', profit_and_loss_statement_views, name='profit_and_loss_statement_views'),

]