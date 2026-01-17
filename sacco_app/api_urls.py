from django.urls import path
from sacco_app.api_views import *

urlpatterns = [
    path('category-type/', CategoryTypeAPIView.as_view(), name='category_type_apis'),
    path('category/', CategoryAPIView.as_view(), name='category_apis'),
    path('default-account-setup/', DefaultAccountSetupAPIView.as_view(), name='default_account_setup_apis'),
    path('get-account-list/<str:register_id>/', GetAccountDetailsAPIView.as_view(), name='get_account_details_of_member'),
    path('get-bank-account-list/<str:code>/', GetAccountDetailsByBankidAPIView.as_view(), name='get_account_details_by_bank_id'),
    path('get-account-entry-list/<str:code>/', GetAccountEntryListAPIView.as_view(), name='get_account_entry_list'),
]
