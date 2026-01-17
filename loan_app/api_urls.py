from django.urls import path
from .api_views import *

urlpatterns = [
    path('loan-account-create/', LoanRegistrationAPIView.as_view(), name='category_type_apis'),
    path('loan-account-get/', GetLoanAccountAPIView.as_view(), name='category_type_apis'),
    path('loan-account-get/<str:loan_id>/', GetLoanAccountAPIView.as_view(), name='category_type_apis'),
]
