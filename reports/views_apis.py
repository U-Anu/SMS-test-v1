from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .forms import TrailBalanceReportForm
from .serializers import *
from rest_framework import permissions
from .models import *
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from pesanile_accounting.scripts import validate_transaction_type
from pesanile_accounting.scripts_pr import *
from pesanile_accounting.account_entries import *
from accounting_engine.utils import *
from django.db.models import Q, Sum
class DateWiseReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DateWiseSerializer

    @swagger_auto_schema(request_body=DateWiseSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = DateWiseSerializer(data=request.data)
            if serializer.is_valid():
                start_date = serializer.data.get('start_date')
                end_date = serializer.data.get('end_date')
                print('Company Id ',request.user.company_name.pk)
                obj = AccountEntry.objects.filter(Q(entry_date__range=[start_date, end_date]) & Q(company_id=request.user.company_name.pk))
                serializer = DateWiseAccountEntrySerializer(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class PayableReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PayableReportSerializer

    @swagger_auto_schema(request_body=PayableReportSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = PayableReportSerializer(data=request.data)
            if serializer.is_valid():
                payable = serializer.data.get('payable')
                obj = AccountEntry.objects.filter(Q(ref_no=payable) & Q(company_id=request.user.company_name.pk))
                serializer = PayableAccountEntrySerializer(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class ReceivableReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReceivableReportSerializer

    @swagger_auto_schema(request_body=ReceivableReportSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = ReceivableReportSerializer(data=request.data)
            if serializer.is_valid():
                receivable = serializer.data.get('receivable')
                obj = AccountEntry.objects.filter(Q(ref_no=receivable) & Q(company_id=request.user.company_name.pk))
                serializer = ReceivableAccountEntrySerializer(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class CustomTransactionDetailByTransactionIdAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTransactionDetailByTransactionIdSerializer

    @swagger_auto_schema(request_body=CustomTransactionDetailByTransactionIdSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = CustomTransactionDetailByTransactionIdSerializer(data=request.data)
            if serializer.is_valid():
                transaction_id = serializer.data.get('transaction_id')
                obj = CustomTransactionDetail.objects.filter(transaction_id=transaction_id)
                serializer = CustomTransactionDetailSerializer(obj, many=True)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class TrailBalanceReportAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TrailBalanceReportSerializer

    @swagger_auto_schema(request_body=TrailBalanceReportSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TrailBalanceReportSerializer(data=request.data)
            if serializer.is_valid():
                user_details = request.user
                company_id = user_details.company_name.pk
                start_date = serializer.data.get('start_date')
                end_date = serializer.data.get('end_date')
                acc_obj = Accounts.objects.filter(company_id=company_id).only('account_number')
                my_list = []
                for data in acc_obj:
                    print(data)
                    acc_ent_obj = AccountEntry.objects.filter(Q(account_number=data)&Q(entry_date__range=(start_date,end_date)))
                    total_debit = acc_ent_obj.filter(debit_credit_marker='Debit').aggregate(Sum('amount')).get('amount__sum')
                    print('total_debit ', total_debit)
                    total_credit = acc_ent_obj.filter(debit_credit_marker='Credit').aggregate(Sum('amount')).get('amount__sum')
                    my_dict = {
                        'account_id': str(data.pk),
                        'account_number': str(data),
                        'debit_amount': 0 if total_debit is None else total_debit,
                        'credit_amount': 0 if total_credit is None else total_credit ,
                    }
                    my_list.append(my_dict)
                return Response(data=my_list, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class GeneralLedgerWithDiffSubLedgersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GeneralLedgerWithDiffSubLedgersSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_details = request.user
            company_id = user_details.company_name.pk
            # start_date = serializer.data.get('start_date')
            # end_date = serializer.data.get('end_date')
            acc_obj = Accounts.objects.filter(company_id=company_id).only('gl_line')
            my_list = []
            for data in acc_obj:
                print(data)
                acc_ent_obj = AccountEntry.objects.filter(account_number=data)
                for data in acc_ent_obj:
                    my_dict = {
                        'account_id': str(data.account_number.pk),
                        'account_number': str(data.account_number),
                        'transaction_date': data.entry_date,
                        'amount': data.amount,
                        'debit_credit_marker': data.debit_credit_marker,
                    }
                    my_list.append(my_dict)
            return Response(data=my_list, status=status.HTTP_200_OK)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class ReceivableListingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReceivableListingSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_details = request.user
            company_id = user_details.company_name.pk
            print('company_id ',company_id)
            obj = AccountReceivable.objects.filter(company_id=company_id)
            serializer = ReceivableListingSerializer(obj, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class AccountPayableAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountPayableSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_details = request.user
            company_id = user_details.company_name.pk
            print('company_id ',company_id)
            obj = AccountPayable.objects.filter(company_id=company_id)
            serializer = AccountPayableSerializer(obj, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class StatementOfCashFlowAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            user_details = request.user
            company_id = user_details.company_name.pk
            print('company_id ',company_id)
            acc_obj_expense = Accounts.objects.filter(Q(company_id=company_id)&Q(account_category__name='Expense'))
            acc_obj_income = Accounts.objects.filter(Q(company_id=company_id)&Q(account_category__name='Income'))
            my_list = []
            print('acc_obj_expense count ',acc_obj_expense, acc_obj_expense.count())
            print('acc_obj_income count ',acc_obj_income, acc_obj_income.count())
            if acc_obj_expense.exists():
                for data in acc_obj_expense:
                    my_dict = {
                        'account_id' : data.account_id,
                        'account_number' : data.account_number,
                        'amount' : data.total_balance,
                        'account_category' : data.account_category.name,
                        'type' : 'Payment',
                        'last_updated_at': data.updated_at
                    }
                    my_list.append(my_dict) 

            if acc_obj_income.exists():
                for data in acc_obj_income:
                    my_dict = {
                        'account_id' : data.account_id,
                        'account_number' : data.account_number,
                        'amount' : data.total_balance,
                        'account_category': data.account_category.name,
                        'type' : 'Receipt',
                        'last_updated_at': data.updated_at
                    }
                    my_list.append(my_dict)
            return Response(data=my_list, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class StatementOfReceiptAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatementOfReceiptSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_details = request.user
            print('user_details ',user_details)
            company_id = user_details.company_name.pk
            print('company_id ',company_id)
            obj = Receipt.objects.filter(company_id=company_id)
            print('obj ',obj)
            serializer = StatementOfReceiptSerializer(obj, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class StatementOfPaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = StatementOfPaymentSerializer

    def get(self, request, *args, **kwargs):
        try:
            user_details = request.user
            company_id = user_details.company_name.pk
            obj = Payment.objects.filter(company_id=company_id)
            serializer = StatementOfPaymentSerializer(obj, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
