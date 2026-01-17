from django.urls import path
from .view_update_delete import *
urlpatterns = [
    path('branch-update/<pk>/', branch_update, name='branch_update'),
    path('branch-delete/<pk>/', branch_delete, name='branch_delete'),

    path('currency-update/<pk>/', currency_update, name='currency_update'),
    path('currency-delete/<pk>/', currency_delete, name='currency_delete'),

    path('company-update/<pk>/', company_update, name='company_update'),
    path('company-delete/<pk>/', company_delete, name='company_delete'),

    path('asset-type-update/<pk>/', asset_type_update, name='asset_type_update'),
    path('asset-type-delete/<pk>/', asset_type_delete, name='asset_type_delete'),

    path('glline-update/<pk>/', glline_update, name='glline_update'),
    path('glline-delete/<pk>/', glline_delete, name='glline_delete'),

    path('asset-type-update/<pk>/', asset_type_update, name='asset_type_update'),
    path('asset-type-delete/<pk>/', asset_type_delete, name='asset_type_delete'),

    path('transaction-code-update/<pk>/', transaction_code_update, name='transaction_code_update'),
    path('transaction-code-delete/<pk>/', transaction_code_delete, name='transaction_code_delete'),

    path('transaction-type-mode-update/<pk>/', transaction_type_mode_update, name='transaction_type_mode_update'),
    path('transaction-type-mode-delete/<pk>/', transaction_type_mode_delete, name='transaction_type_mode_delete'),


    path('account-category-update/<pk>/', account_category_update, name='account_category_update'),
    path('account-category-delete/<pk>/', account_category_delete, name='account_category_delete'),

    path('account-restriction-update/<pk>/', account_restriction_update, name='account_restriction_update'),
    path('account-restriction-delete/<pk>/', account_restriction_delete, name='account_restriction_delete'),

    path('account-type-category-update/<pk>/', account_type_category_update, name='account_type_category_update'),
    path('account-type-category-delete/<pk>/', account_type_category_delete, name='account_type_category_delete'),

    path('account-type-update/<pk>/', account_type_update, name='account_type_update'),
    path('account-type-delete/<pk>/', account_type_delete, name='account_type_delete'),

    path('account-update/<pk>/', account_update, name='account_update'),
    path('account-delete/<pk>/', account_delete, name='account_delete'),

    path('reference-type-update/<pk>/', reference_type_update, name='reference_type_update'),
    path('reference-type-delete/<pk>/', reference_type_delete, name='reference_type_delete'),

    path('payment-complexity-update/<pk>/', payment_complexity_update, name='payment_complexity_update'),
    path('payment-complexity-delete/<pk>/', payment_complexity_delete, name='payment_complexity_delete'),

]
