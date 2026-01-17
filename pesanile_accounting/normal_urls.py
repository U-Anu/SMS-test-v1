from django.urls import path
from .normal_views import *
urlpatterns = [
    path('dashboard-finance/', dashboard_finance, name='dashboard_finance'),
    path('check-transaction-type/', check_transaction_type, name='check_transaction_type'),
    path('get-accounts-by-currency-and-transaction/<str:currency_id>/<txn_type_id>/', get_acc_by_currency_and_txn_type_id, name='get_acc_by_currency_and_txn_type_id'),

    # path('check-transaction-type/<int:transaction_type_id>/', check_transaction_type, name='check_transaction_type'),
    path('get-account-by-currency/<int:currency_id>/', get_account_by_currency, name='get_account_by_currency'),

    path('get-account-currency/<int:account_id>/', get_account_currency, name='get_account_currency'),
    path('service-payment/', service_payment, name='service_payment'),

    path('service-payments-create/', service_payment_create, name='service_payment_create'),
    path('service-payments-list/', service_payment_list, name='service_payment_list'),

    path('transaction-list/', transaction_list, name='transaction_list'),
    path('transaction-create/', transaction_create, name='transaction_create'),
    path('special-transaction-create/<str:special_txn>/', special_transaction_create, name='special_transaction_create'),

    path('account-list/', account_list, name='account_list'),
    path('account-create/', account_create, name='account_create'),

    # Above Done

    path('account-restriction-list/', account_restriction_list, name='account_restriction_list'),
    path('account-restriction-create/', account_restriction_create, name='account_restriction_create'),

    path('overdraft-limit-list/', overdraft_limit_list, name='overdraft_limit_list'),
    path('overdraft-limit-create/', overdraft_limit_create, name='overdraft_limit_create'),

    path('glline-list/', glline_list, name='glline_list'),
    path('glline-create/', glline_create, name='glline_create'),

    path('asset-type-list/', asset_type_list, name='asset_type_list'),
    path('asset-type-create/', asset_type_create, name='asset_type_create'),

    path('account-holder-list/', account_holder_list, name='account_holder_list'),
    path('account-holder-create/', account_holder_create, name='account_holder_create'),

    path('account-category-list/', account_category_list, name='account_category_list'),
    path('account-category-create/', account_category_create, name='account_category_create'),

    path('account-type-list/', account_type_list, name='account_type_list'),
    path('account-type-create/', account_type_create, name='account_type_create'),

    path('exchange-rate-list/', exchange_rate_list, name='exchange_rate_list'),
    path('exchange-rate-create/', exchange_rate_create, name='exchange_rate_create'),

    path('currency-list/', currency_list, name='currency_list'),
    path('currency-create/', currency_create, name='currency_create'),

    path('company-list/', company_list, name='company_list'),
    path('company-create/', company_create, name='company_create'),
    path('company-update/<pk>/', company_update, name='company_update'),

    path('branch-list/', branch_list, name='branch_list'),
    path('branch-create/', branch_create, name='branch_create'),

    path('transaction-code-list/', transaction_code_list, name='transaction_code_list'),
    path('transaction-code-create/', transaction_code_create, name='transaction_code_create'),

    path('charge-code-classification-list/', charge_code_classification_list, name='charge_code_classification_list'),
    path('charge-code-classification-create/', charge_code_classification_create, name='charge_code_classification_create'),


    path('charge-code-list/', charge_code_list, name='charge_code_list'),
    path('charge-code-create/', charge_code_create, name='charge_code_create'),

    path('interest-code-list/', interest_code_list, name='interest_code_list'),
    path('interest-code-create/', interest_code_create, name='interest_code_create'),



    path('transaction-type-list/', transaction_type_list, name='transaction_type_list'),
    path('transaction-type-create/', transaction_type_create, name='transaction_type_create'),

    path('transaction-details-list/', transaction_details_list, name='transaction_details_list'),
    path('transaction-details-create/', transaction_details_create, name='transaction_details_create'),

    path('account-entry-list/', account_entry_list, name='account_entry_list'),
    path('account-entry-create/', account_entry_create, name='account_entry_create'),

    path('teller-profile-list/', teller_profile_list, name='teller_profile_list'),
    path('teller-profile-create/', teller_profile_create, name='teller_profile_create'),

    # Account Receivable and Payable

    path('account-receivable-list/', account_receivable_list, name='account_receivable_list'),
    path('account-receivable-create/', account_receivable_create, name='account_receivable_create'),

    path('account-payable-list/', account_payable_list, name='account_payable_list'),
    path('account-payable-create/', account_payable_create, name='account_payable_create'),

    path('payment-list/', payment_list, name='payment_list'),
    path('payment-create/', payment_create, name='payment_create'),

    path('receipt-list/', receipt_list, name='receipt_list'),
    path('receipt-create/', receipt_create, name='receipt_create'),

    path('txn-type-cls-list/', transaction_type_classification_list, name='transaction_type_classification_list'),
    path('txn-type-cls-create/', transaction_type_classification_create, name='transaction_type_classification_create'),

    path('txn-type-mode-list/', transaction_type_mode_list, name='transaction_type_mode_list'),
    path('txn-type-mode-create/', transaction_type_mode_create, name='transaction_type_mode_create'),

    path('payment-complexity-list/', payment_complexity_list, name='payment_complexity_list'),
    path('payment-complexity-create/', payment_complexity_create, name='payment_complexity_create'),

    path('reference-type-list/', reference_type_list, name='reference_type_list'),
    path('reference-type-create/', reference_type_create, name='reference_type_create'),

    path('rec-and-pay-transaction/<str:special_txn>/', receivable_and_payable_transaction, name='receivable_and_payable_transaction'),

    path('user-financial-accounting-mapping-list/', user_financial_accounting_mapping_list, name='user_financial_accounting_mapping_list'),
    path('user-financial-accounting-mapping-create/', user_financial_accounting_mapping_create, name='user_financial_accounting_mapping_create'),

    path('user-financial-accounting-category-list/', user_financial_accounting_category_list, name='user_financial_accounting_category_list'),
    path('user-financial-accounting-category-create/', user_financial_accounting_category_create, name='user_financial_accounting_category_create'),

    path('post-receivable-and-payable-transaction-create/', post_receivable_and_payable_transaction, name='post_receivable_and_payable_transaction'),

    path('direct-payment-list/', direct_payment_list, name='direct_payment_list'),
    path('account-payment-create/', account_payment_create, name='account_payment_create'),

    path('account-receipt-create/', account_receipt_create, name='account_receipt_create'),
    path('direct-receipt-list/', direct_receipt_list, name='direct_receipt_list'),

    path('custom-field-create/', custom_field_create, name='custom_field_create'),
    path('custom-field-list/', custom_field_list, name='custom_field_list'),

    path('custom-field-type-create/', custom_field_type_create, name='custom_field_type_create'),
    path('custom-field-type-list/', custom_field_type_list, name='custom_field_type_list'),

    path('custom-transaction-field-mapping-create/', custom_transaction_field_mapping_create, name='custom_transaction_field_mapping_create'),
    path('custom-transaction-field-mapping-list/', custom_transaction_field_mapping_list, name='custom_transaction_field_mapping_list'),

    path('custom-transaction-details-list/', custom_transaction_detail_list, name='custom_transaction_detail_list'),


    path('bank_detail_list/', bank_detail_list, name='bank_detail_list'),
    path('bank_detail_list_create/', bank_detail_create, name='bank_detail_create'),
    path('bank_detail_list_update/<int:pk>/', bank_detail_update, name='bank_detail_update'),
    path('bank_detail_list_delete/<int:pk>/', bank_detail_delete, name='bank_detail_delete'),


    # Asset type category
    path('asset-type-category-create/', asset_type_category_create, name='asset_type_category_create'),
    path('asset-type-category-list/', asset_type_category_list, name='asset_type_category_list'),
    path('asset-type-category-update/', asset_type_category_update, name='asset_type_category_update'),
    path('asset-type-category-delete/', asset_type_category_delete, name='asset_type_category_delete'),
    # Account type category
    path('account-type-category-create/', account_type_category_create, name='account_type_category_create'),
    path('account-type-category-list/', account_type_category_list, name='account_type_category_list'),
    # Business Group
    path('business-group-create/', business_group_create, name='business_group_create'),
    path('business-group-list/', business_group_list, name='business_group_list'),
    # Department
    path('department-create/', department_create, name='department_create'),
    path('department-list/', department_list, name='department_list'),

]