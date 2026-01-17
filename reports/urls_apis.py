from django.urls import path
from reports.views_apis import *

urlpatterns = [
    path('date-wise/',DateWiseReportAPIView.as_view(), name='txn_date_wise'),
    path('payable-report/',PayableReportAPIView.as_view(), name='payable_report'),
    path('receivable-report/',ReceivableReportAPIView.as_view(), name='receivable_report'),
    path('custom-transaction-details-by-txn-id/',CustomTransactionDetailByTransactionIdAPIView.as_view(), name='custom_transaction_details_by_txn_id'),

    # Trail balance report
    path('trail-balance-report/', TrailBalanceReportAPIView.as_view(), name='trail_balance_report_api_view'),
    path('general-ledger-with-diff-sub-ledger/', GeneralLedgerWithDiffSubLedgersAPIView.as_view(), name='general_ledger_with_diff_sub_ledgers'),
    path('receivable-listing/', ReceivableListingAPIView.as_view(), name='receivable_listing_apis'),
    path('payable-listing/', AccountPayableAPIView.as_view(), name='payable_listing_apis'),
    path('statement-of-cashflow/', StatementOfCashFlowAPIView.as_view(), name='statement_of_cashflow_apis'),
    path('statement-of-receipt/', StatementOfReceiptAPIView.as_view(), name='statement_of_receipt_apis'),
    path('statement-of-payment/', StatementOfPaymentAPIView.as_view(), name='statement_of_payment_apis'),

]