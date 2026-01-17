from django.urls import path
from .views import *
from .dynamic_report import *
urlpatterns = [
    path('date-wise/', date_wise, name='date_wise'),
    path('transaction-id-wise/', transaction_id_wise, name='transaction_id_wise'),
    path('account-wise/', account_wise, name='account_wise'),
    path('transaction_journal-wise/', transaction_journal, name='transaction_journal'),
    path('dutymeal-wise/', dutymeal_wise, name='dutymeal_wise'),
    path('teller-wise/', teller_wise, name='teller_wise'),
    path('txn-code-wise/', transaction_code_wise, name='transaction_code_wise'),
    path('till-wise/', till_wise, name='till_wise'),
    path('company-wise/', company_wise, name='company_wise'),
    path('trail-balance/', trail_balance_report, name='trail_balance'),
    path('glline-with-diff-sub-glline/', general_ledger_with_diff_sub_ledgers, name='general_ledger_with_diff_sub_ledgers_report'),
    path('receivable-listing-report/', receivable_listing, name='receivable_listing_report'),
    path('payable-listing-report/', account_payable_listing, name='account_payable_listing_report'),
    path('statement-of-cashflow-report/', statement_of_cash_flow, name='statement_of_cash_flow_report'),
    path('statement-of-receipt/', statement_of_receipt, name='statement_of_receipt'),
    path('statement-of-payment/', statement_of_payment, name='statement_of_payment'),
    path('report-type/add/', report_type_create, name='report_type_add'),
    path('report-type/', report_type_list, name='report_type_list'),
    path('reportmapping/add/', reportmapping_create, name='reportmapping_add'),
    path('reportmapping/', reportmapping_list, name='reportmapping_list'),
]
