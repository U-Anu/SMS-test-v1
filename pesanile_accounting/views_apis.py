from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from .models import Transaction, TransactionType, TellerProfile
from rest_framework import permissions
from .models import *
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password
from .scripts import validate_transaction_type
from .scripts_pr import *
from .account_entries import *
from accounting_engine.utils import *
from .tenant_ways import *

def common_input_params_validate(company_id, transaction_type_id, input_params_values):
    input_params_key = list(input_params_values.keys())
    input_params_value = list(input_params_values.values())
    resp = validate_mapped_custom_transaction_field(company_id, transaction_type_id)
    if not resp[0]:
        # print('thsi is error....')
        message = response_message('Failed', message=f"""{resp[1]}""")
        resp = [False, message]
        return resp
    custom_mapped_field_optional = resp[1]
    custom_mapped_field_mandatory = resp[2]
    custom_mapped_field_type_optional = resp[3]
    custom_mapped_field_type_mandatory = resp[4]
    if not set(custom_mapped_field_mandatory).issubset(set(input_params_key)):
        missing_parameters = set(custom_mapped_field_mandatory) - set(input_params_key)
        message = response_message('Failed', message=f"""Here, input parameters are missing => {missing_parameters}""")
        resp = [False, resp[5]]
        # return Response(data=resp[5], status=status.HTTP_400_BAD_REQUEST)
        return resp
    # validate parameters values
    resp = check_field_validation_value(company_id, transaction_type_id, input_params_key, input_params_value)
    print('common_input_params_validate ===> resp ', resp)
    if len(resp) != 0:
        resp = [False,resp]
        return resp
    else:
        resp = [True, resp]
        return resp
def update_custom_transaction_details(transaction_id,company_id, key_list, value_list, user_id=None):
    try:
        for key, value in zip(key_list, value_list):
            obj = CustomTransactionDetail.objects.create(
                transaction_id=transaction_id,
                custom_field_id=CustomField.objects.get(field_name=key),
                field_value=value,
                company_name=company_id,
                created_by=user_id,
            )
            print('obj', obj)
        return [True,'Successfully Created...']
    except Exception as error:
        print('ERROR : update_custom_transaction_details ',error)
        return [False, f'''{error}''']


class TransactionCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionSimpleSerializer

    @swagger_auto_schema(request_body=TransactionSimpleSerializer)
    def post(self, request, *args, **kwargs):
        serializer = TransactionSimpleSerializer(data=request.data)
        if serializer.is_valid():
            logged_user_details = request.user.company_name
            local_currency = logged_user_details.local_currency
            transaction_type = str(serializer.validated_data.get('transaction_type'))
            from_account_id = str(request.data.get('from_account_id'))
            from_currency_id = str(request.data.get('from_currency_id'))

            # Extract necessary fields
            fc_id = request.data.get('from_currency_id')
            tc_id = request.data.get('to_currency_id')
            from_amount = request.data.get('from_amount')
            to_account_id = request.data.get('to_account_id')
            to_currency_id = serializer.validated_data.get('to_currency_id')
            charges_applied = request.data.get('charges_applied')

            teller_profile = TellerProfile.objects.get(user=request.user)
            is_teller = teller_profile.can_process_transaction(float(from_amount), str(transaction_type))
            if not is_teller[0]:
                message = response_message('Failed', message=is_teller[1])
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            get_ex_rate = get_exchange_rate(str(from_currency_id), str(to_currency_id),
                                            base_currency=str(local_currency))
            if not get_ex_rate[0]:
                message = response_message('Failed', message=get_ex_rate[1])
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
            txn_type_obj = TransactionType.objects.get(name=transaction_type)
            dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
            cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
            credit_amount = float(from_amount) * float(ex_rate)
            entry_type = 'PL'
            transaction_id = generate_txn_id()
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount,
                                 credit_currency=tc_id,
                                 total_debit_amt=float(from_amount), debit_currency=fc_id,
                                 dr_acc=from_account_id,
                                 cr_acc=to_account_id,
                                 debit_credit_marker='DebitCredit', user=request.user.pk)

            if not resp:
                message = response_message('Failed', message='Transaction failed')
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(
                transaction_id=transaction_id,
                exchange_rate_calc_mode=res_cal_mode,
                exchange_rate_used_id=ex_rate_id,
                to_amount=credit_amount,
                status='success'
            )
            teller_profile.clear_teller_amount(float(from_amount), str(transaction_type))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialTransactionCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SpecialTransactionSerializer

    @swagger_auto_schema(request_body=SpecialTransactionSerializer)
    def post(self, request, special_txn):
        serializer = SpecialTransactionSerializer(data=request.data)
        if serializer.is_valid():
            logged_user_details = request.user.company_name
            local_currency = logged_user_details.local_currency
            transaction_type = str(serializer.validated_data.get('transaction_type'))
            from_account_id = str(request.data.get('from_account_id'))
            from_currency_id = str(serializer.validated_data.get('from_currency_id'))
            fc_id = request.data.get('from_currency_id')
            tc_id = request.data.get('to_currency_id')
            from_amount = request.data.get('from_amount')
            to_account_id = request.data.get('to_account_id')
            to_currency_id = serializer.validated_data.get('to_currency_id')
            charges_applied = request.data.get('charges_applied')

            teller_profile = TellerProfile.objects.get(user=request.user)
            is_teller = teller_profile.can_process_transaction(float(from_amount), str(transaction_type))
            if not is_teller[0]:
                message = response_message('Failed', message=is_teller[1])
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            get_ex_rate = get_exchange_rate(str(from_currency_id), str(to_currency_id),
                                            base_currency=str(local_currency))
            if not get_ex_rate[0]:
                message = response_message('Failed', message=get_ex_rate[1])
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
            txn_type_obj = TransactionType.objects.get(pk=special_txn)
            dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
            cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
            credit_amount = float(from_amount) * float(ex_rate)
            entry_type = 'PL'
            transaction_id = generate_txn_id()
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount,
                                 credit_currency=tc_id,
                                 total_debit_amt=float(from_amount), debit_currency=fc_id,
                                 dr_acc=from_account_id,
                                 cr_acc=to_account_id,
                                 debit_credit_marker='DebitCredit', user=request.user.pk)

            if not resp:
                message = response_message('Failed', message="Transaction failed")
                return Response(message, status=status.HTTP_400_BAD_REQUEST)

            serializer.save(
                transaction_id=transaction_id,
                exchange_rate_calc_mode=res_cal_mode,
                exchange_rate_used_id=ex_rate_id,
                to_amount=credit_amount,
                status='success'
            )
            teller_profile.clear_teller_amount(float(from_amount), str(transaction_type))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountReceivableAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountReceivableSerializer

    @swagger_auto_schema(responses={200: AccountReceivableSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = AccountReceivable.objects.filter(~Q(payment_status='Paid'))
            serializer = AccountReceivableSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"""{error}""")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountReceivableSerializer)
    def post(self, request, *args, **kwargs):
        try:
            print('its okay...')
            serializer = AccountReceivableSerializer(data=request.data)
            if serializer.is_valid():
                print('its okay', request.user.company_name)
                obj = serializer.save()
                tenant_create_save(obj,user=request.user,company=request.user.company_name, branch=request.user.branch_name)
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            print('error..')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"""{error}""")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountReceivableAmountSerializer)
    def put(self, request, reference_number, *args, **kwargs):
        try:
            instance = AccountReceivable.objects.get(reference_number=reference_number)
            serializer = AccountReceivableAmountSerializer(data=request.data)
            if serializer.is_valid():
                print("request.data.get('new_amount') ",request.data.get('new_amount'))
                new_amount = eval(request.data.get('new_amount'))
                instance.actual_amount = instance.actual_amount + new_amount
                get_due_amount = instance.amount_due
                if get_due_amount != 0:
                    get_due_amount = get_due_amount + new_amount
                instance.amount_due = get_due_amount
                instance.save()
                message = response_message('Success', message="Record updated successfully.")
                return Response(data=message, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except AccountReceivable.DoesNotExist:
            message = response_message('Failed', message="Record not found.")
            return Response(data=message, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            message = response_message('Failed', message=f"""{error}""")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class CompanyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanySerializer

    @swagger_auto_schema(responses={200: CompanySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = Company.objects.all()
            serializer = CompanySerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CompanySerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = CompanySerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class CompanyUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CompanySerializer

    @swagger_auto_schema(request_body=CompanySerializer)
    def put(self, request, pk, *args, **kwargs):
        try:
            # Retrieve the existing object using the primary key
            obj = Company.objects.get(pk=pk)
            # Pass the existing object instance and request data to the serializer
            serializer = CompanySerializer(obj, data=request.data)
            if serializer.is_valid():
                # Save the updated object with the current user as the updater
                obj = serializer.save(created_by=request.user)
                message = response_message('Success', message="Update Successful", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Company.DoesNotExist:
            # Handle the case where the object does not exist
            message = response_message('Failed', message="Company not found")
            return Response(data=message, status=status.HTTP_404_NOT_FOUND)
        except Exception as error:
            # Catch and return any other exceptions
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)



class BranchAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BranchSerialize

    @swagger_auto_schema(responses={200: BranchSerialize(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = Branch.objects.all()
            serializer = BranchSerialize(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=BranchSerialize)
    def post(self, request, *args, **kwargs):
        try:
            serializer = BranchSerialize(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class AccountTypeAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountTypeSerializer

    @swagger_auto_schema(responses={200: AccountTypeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = AccountType.objects.all()
            serializer = AccountTypeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountTypeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AccountTypeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class AccountCategoryAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AccountCategorySerializer

    @swagger_auto_schema(responses={200: AccountCategorySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = AccountCategory.objects.all()
            serializer = AccountCategorySerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountCategorySerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AccountCategorySerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class AccountHolderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountHolderSerializer

    @swagger_auto_schema(responses={200: AccountHolderSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = AccountHolder.objects.all()
            serializer = AccountHolderSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountHolderSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AccountHolderSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class AssetTypeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AssetTypeSerializer

    @swagger_auto_schema(responses={200: AssetTypeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = AssetType.objects.all()
            serializer = AssetTypeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AssetTypeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AssetTypeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class GLLineAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GLLineSerializer

    @swagger_auto_schema(responses={200: GLLineSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = GLLine.objects.all()
            serializer = GLLineSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=GLLineSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = GLLineSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class AccountsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountsSerializer

    @swagger_auto_schema(responses={200: AccountsSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            company_id = request.user.company_name.pk
            records = Accounts.objects.filter(company_id=company_id)
            serializer = AccountsSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountsSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AccountsSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class OverdraftLimitAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OverdraftLimitSerializer

    @swagger_auto_schema(responses={200: OverdraftLimitSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = OverdraftLimit.objects.all()
            serializer = OverdraftLimitSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=OverdraftLimitSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = OverdraftLimitSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class AccountRestrictionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountRestrictionSerializer

    @swagger_auto_schema(responses={200: AccountRestrictionSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = AccountRestriction.objects.all()
            serializer = AccountRestrictionSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountRestrictionSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AccountRestrictionSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class TransactionCodeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionCodeSerializer

    @swagger_auto_schema(responses={200: TransactionCodeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = TransactionCode.objects.all()
            serializer = TransactionCodeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TransactionCodeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TransactionCodeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class CurrencyAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CurrencySerializer

    @swagger_auto_schema(responses={200: CurrencySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = Currency.objects.all()
            serializer = CurrencySerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CurrencySerializer)
    def post(self, request, *args, **kwargs):
        try:
            # serializer = CurrencySerializer(data=request.data)
            serializer = request.data
            currency_code = serializer.get('currency_code')
            currency_name = serializer.get('currency_name')
            symbol = serializer.get('symbol')
            currency_obj, created = Currency.objects.get_or_create(
                currency_code=currency_code,
                defaults={'currency_name': currency_name, 'symbol': symbol}
            )
            print('currency_obj ',currency_obj)
            print('Created ', created)
            if not created:
                currency_obj.currency_name = currency_name
                currency_obj.symbol = symbol
                currency_obj.save()
                message = response_message('Success', message="Success", record_id=currency_obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            else:
                message = response_message('Success', message="Success", record_id=currency_obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)

        except Exception as error:

            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class ChargeCodeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChargeCodeSerializer

    @swagger_auto_schema(responses={200: ChargeCodeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = ChargeCode.objects.all()
            serializer = ChargeCodeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ChargeCodeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = ChargeCodeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class TransactionTypeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionTypeSerializer

    @swagger_auto_schema(responses={200: TransactionTypeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = TransactionType.objects.all()
            serializer = TransactionTypeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TransactionTypeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TransactionTypeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class TransactionTypeClassificationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionTypeClassificationSerializer

    @swagger_auto_schema(responses={200: TransactionTypeClassificationSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = TransactionTypeClassification.objects.all()
            serializer = TransactionTypeClassificationSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TransactionTypeClassificationSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TransactionTypeClassificationSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class TransactionTypeModeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionTypeModeSerializer

    @swagger_auto_schema(responses={200: TransactionTypeModeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = TransactionTypeMode.objects.all()
            serializer = TransactionTypeModeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TransactionTypeModeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TransactionTypeModeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TransactionDetailSerializer

    @swagger_auto_schema(responses={200: TransactionDetailSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = TransactionDetail.objects.all()
            serializer = TransactionDetailSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TransactionDetailSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TransactionDetailSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class TellerProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TellerProfileSerializer

    @swagger_auto_schema(responses={200: TellerProfileSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = TellerProfile.objects.all()
            serializer = TellerProfileSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TellerProfileSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = TellerProfileSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class ReferenceTypeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReferenceTypeSerializer

    @swagger_auto_schema(responses={200: ReferenceTypeSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = ReferenceType.objects.all()
            serializer = ReferenceTypeSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ReferenceTypeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = ReferenceTypeSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class PaymentComplexityAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentComplexitySerializer

    @swagger_auto_schema(responses={200: PaymentComplexitySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = PaymentComplexity.objects.all()
            serializer = PaymentComplexitySerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PaymentComplexitySerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = PaymentComplexitySerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class AccountPayableAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AccountPayableSerializer

    @swagger_auto_schema(responses={200: AccountPayableSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = AccountPayable.objects.filter(~Q(payment_status='Paid'))
            serializer = AccountPayableSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=AccountPayableSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AccountPayableSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                tenant_create_save(obj, user=request.user, company=request.user.company_name,
                                   branch=request.user.branch_name)

                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class PaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentSerializer

    @swagger_auto_schema(responses={200: PaymentSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = Payment.objects.all()
            serializer = PaymentSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = PaymentSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class ReceiptAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReceiptSerializer

    @swagger_auto_schema(responses={200: ReceiptSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = Receipt.objects.all()
            serializer = ReceiptSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=ReceiptSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = ReceiptSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class UserFinancialAccountMappingAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFinancialAccountMappingSerializer

    @swagger_auto_schema(responses={200: UserFinancialAccountMappingSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = UserFinancialAccountMapping.objects.all()
            serializer = UserFinancialAccountMappingSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserFinancialAccountMappingSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserFinancialAccountMappingSerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class UserFinancialAccountCategoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserFinancialAccountCategorySerializer

    @swagger_auto_schema(responses={200: UserFinancialAccountCategorySerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = UserFinancialAccountCategory.objects.all()
            serializer = UserFinancialAccountCategorySerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserFinancialAccountCategorySerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserFinancialAccountCategorySerializer(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    @swagger_auto_schema(responses={200: UserListSerializer(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = User.objects.all()
            serializer = UserListSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # Manually hash the password before saving
                password = make_password(serializer.validated_data['password'])
                user_data = serializer.validated_data
                user_data['password'] = password

                # Create the user with hashed password
                user = User.objects.create(**user_data)
                print('user ',user)
                message = {"status": "Success", "message": "Its Success"}
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class ReceivableAndPayableTransactionAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PaymentAndReceiptSerializer

    @swagger_auto_schema(request_body=PaymentAndReceiptSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = PaymentAndReceiptSerializer(data=request.data)
            if serializer.is_valid():
                transaction_type = serializer.validated_data.get('transaction_type')
                input_params_values = serializer.validated_data.get('input_params_values')
                get_txn_obj = validate_transaction_type(transaction_type)

                if get_txn_obj is None:
                    return Response({'message': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

                transaction_type_id = get_txn_obj.pk
                receivable = serializer.validated_data.get('receivable')
                payable = serializer.validated_data.get('payable')
                amount = float(serializer.validated_data.get('amount'))
                company_id = request.user.company_name
                print('ins okay')
                resp = common_input_params_validate(company_id, transaction_type_id, input_params_values)
                print('resp ',resp)
                if not resp[0]:
                    return Response(data=resp[1], status=status.HTTP_400_BAD_REQUEST)

                print('='*30)
                print('check..')
                print('company_id ',company_id)
                if receivable is None and payable is None:
                    return Response({'message': 'Receivable and payable should not be empty'}, status=status.HTTP_400_BAD_REQUEST)
                if get_txn_obj.name.lower() == 'payment' and payable is None:
                    return Response({'message': 'Kindly select the payable'}, status=status.HTTP_400_BAD_REQUEST)
                if get_txn_obj.name.lower() == 'receipt' and receivable is None:
                    return Response({'message': 'Kindly select the receivable'}, status=status.HTTP_400_BAD_REQUEST)

                if get_txn_obj.name.lower() == 'payment':
                    result = apply_payment_to_payable(payable, amount,company_id)
                    if not result[0]:
                        return Response({'message': result[1]}, status=status.HTTP_400_BAD_REQUEST)
                if get_txn_obj.name.lower() == 'receipt':
                    result = apply_payment_to_receivable(receivable, amount,company_id)
                    if not result[0]:
                        return Response({'message': result[1]}, status=status.HTTP_400_BAD_REQUEST)

                account_category = get_txn_obj.category_of_account.account_category_id
                print('account_category ',account_category)
                dr_obj = Accounts.objects.filter(Q(company_name=company_id)&Q(account_category_id=account_category))
                if not dr_obj.exists():
                    return Response({'message': 'Company account not found'}, status=status.HTTP_400_BAD_REQUEST)
                dr_acc = dr_obj.last().pk

                if get_txn_obj.name.lower() == 'receipt':
                    cr_obj = Accounts.objects.filter(Q(company_name=company_id) | Q(account_category__name__iexact='Income'))
                    if not cr_obj.exists():
                        return Response({'message': 'Company Income account not found'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    cr_acc = cr_obj.last().pk  # Just fixed credit account id
                if get_txn_obj.name.lower() == 'payment':
                    cr_obj = Accounts.objects.filter(Q(company_name=company_id) & Q(account_category__name='Cashbook'))
                    if not cr_obj.exists():
                        return Response({'message': 'Company Cashbook account not found'},
                                        status=status.HTTP_400_BAD_REQUEST)
                    cr_acc = cr_obj.last().pk  # Just fixed credit account id
                print('its okay')
                logged_user_details = request.user.company_name
                local_currency_name = logged_user_details.local_currency
                local_currency_id = logged_user_details.local_currency.pk

                # teller_profile = TellerProfile.objects.get(user=request.user)
                # is_teller = teller_profile.can_process_transaction(amount, get_txn_obj.name.lower())
                # if not is_teller[0]:
                #     return Response({'message': is_teller[1]}, status=status.HTTP_400_BAD_REQUEST)

                get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                                base_currency=str(local_currency_name))
                if not get_ex_rate[0]:
                    return Response({'message': get_ex_rate[1]}, status=status.HTTP_400_BAD_REQUEST)
                # print('is_teller ',is_teller)
                res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
                print('transaction_type ',transaction_type)
                txn_type_obj = TransactionType.objects.get(name=get_txn_obj.name)
                dr_txn_code = txn_type_obj.debit_transaction_code
                cr_txn_code = txn_type_obj.credit_transaction_code
                credit_amount = amount * ex_rate
                entry_type = 'PL'
                transaction_id = generate_txn_id()
                obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id, amount,
                                                cr_acc, local_currency_id, amount, res_cal_mode, ex_rate_id,
                                                charges_applied=False, status='pending',
                                                user=request.user,
                                                company=request.user.company_name,
                                                branch=request.user.branch_name)
                ref_no = receivable if payable is None else payable
                resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                                     credit_currency=local_currency_id, total_debit_amt=amount, debit_currency=local_currency_id,
                                     dr_acc=dr_acc, cr_acc=cr_acc, debit_credit_marker='DebitCredit',
                                     user=request.user,company=request.user.company_name,ref_no=ref_no,
                                     branch=request.user.branch_name)

                obj.transaction_id = transaction_id
                obj.exchange_rate_calc_mode = res_cal_mode
                obj.exchange_rate_used_id = ex_rate_id
                obj.to_amount = amount
                obj.status = 'success' if resp else 'pending'
                obj.save()

                # teller_profile.clear_teller_amount(amount, get_txn_obj.name.lower())
                # update into Custom Transaction Details tables
                resp = update_custom_transaction_details(transaction_id, company_id, list(input_params_values.keys()), list(input_params_values.values()), user_id=None)
                print('CUSTOM TRANSACTION DETAILS UPDATE RESPONSE ',resp)
                message = response_message('Success', message=f"Its Success, Transaction Id {transaction_id}", record_id=transaction_id)
                return Response(data=message, status=status.HTTP_200_OK)
            else:

                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            return Response(data={'message': f"""Technical error while creating {error}"""}, status=status.HTTP_400_BAD_REQUEST)


class CommonRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CommonRegistrationSerialize

    @swagger_auto_schema(responses={200: CommonRegistrationSerialize(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = CommonRegistration.objects.all()
            serializer = CommonRegistrationSerialize(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=CommonRegistrationSerialize)
    def post(self, request, *args, **kwargs):
        try:
            serializer = CommonRegistrationSerialize(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
def get_charge_amount(charge_mode, charge_value, total_amount):
    if charge_mode == 'flat':
        return charge_value
    if charge_mode == 'percentage':
        return (total_amount*charge_value)/100
def transaction_with_charge(transaction_id,get_charge_code,get_txn_obj,amount,company_id=None, user =None):
    try:
        charge_amount, charge_mode, currency, gl_line_to_credit, transaction_code_to_use = get_charge_code.charge_amount, get_charge_code.charge_mode, get_charge_code.currency, get_charge_code.gl_line_to_credit.gl_line_id, get_charge_code.transaction_code_to_use.transaction_code_id
        print('gl_line_to_credit ',gl_line_to_credit)
        get_gl_acc_no = get_account_number(glline=gl_line_to_credit)
        gl_acc_no = get_gl_acc_no.account_id
        print('gl_acc_no ',gl_acc_no)
        charge_amount = get_charge_amount(charge_mode, charge_amount, amount)
        for dr_acc, cr_acc, dr_cur, cr_cur in zip(eval(get_txn_obj.debit_account),
                                                  eval(get_txn_obj.credit_account),
                                                  eval(get_txn_obj.debit_currency),
                                                  eval(get_txn_obj.credit_currency)):
            dr_txn_code = get_txn_obj.debit_transaction_code.transaction_code_id
            cr_txn_code = get_txn_obj.credit_transaction_code.transaction_code_id
            entry_type = 'PL'
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                 credit_amount=amount - charge_amount,
                                 credit_currency=cr_cur, total_debit_amt=amount,
                                 debit_currency=dr_cur,
                                 dr_acc=dr_acc, cr_acc=cr_acc, debit_credit_marker='DebitCredit',
                                 user=user, company=company_id)
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                 credit_amount=charge_amount,
                                 credit_currency=cr_cur, total_debit_amt=amount,
                                 debit_currency=dr_cur,
                                 dr_acc=dr_acc, cr_acc=gl_acc_no, debit_credit_marker='Credit',
                                 user=user, company=company_id)
        return True
    except Exception as error:
        print('error ', error)
        return False

def transaction_without_charge(transaction_id,get_txn_obj,amount,company_id=None, user =None):
    try:
        for dr_acc, cr_acc, dr_cur, cr_cur in zip(eval(get_txn_obj.debit_account),
                                                  eval(get_txn_obj.credit_account),
                                                  eval(get_txn_obj.debit_currency),
                                                  eval(get_txn_obj.credit_currency)):
            dr_txn_code = get_txn_obj.debit_transaction_code.transaction_code_id
            cr_txn_code = get_txn_obj.credit_transaction_code.transaction_code_id
            entry_type = 'PL'
            resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                 credit_amount=amount,
                                 credit_currency=cr_cur, total_debit_amt=amount,
                                 debit_currency=dr_cur,
                                 dr_acc=dr_acc, cr_acc=cr_acc, debit_credit_marker='DebitCredit',
                                 user=user, company=company_id)
        return True
    except Exception as error:
        print('error ', error)
        return False

class AllTransactionAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AllTransactionSerializer

    @swagger_auto_schema(request_body=AllTransactionSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = AllTransactionSerializer(data=request.data)
            if serializer.is_valid():
                transaction_type_id = serializer.data.get('transaction_type_id')
                company_id = serializer.data.get('company_id')
                amount = serializer.data.get('amount')
                input_params_values = serializer.data.get('input_params_values')
                print('calling...')
                resp = common_input_params_validate(company_id, transaction_type_id, input_params_values)
                if not resp[0]:
                    return Response(data=resp[1], status=status.HTTP_400_BAD_REQUEST)
                print('its okay')
                print('Proceed here', resp)

                get_txn_obj = validate_transaction_type(transaction_type_id)

                if get_txn_obj is None:
                    return Response({'message': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)
                # pre set up
                transaction_id = generate_txn_id()
                user = request.user.pk
                if get_txn_obj.debit_account and get_txn_obj.credit_account:
                    charge_apply = get_txn_obj.charge_code
                    if charge_apply:
                        get_charge_code = get_charge_code_details(charge_apply.pk)
                        if get_charge_code is None:
                            return Response(data={"message": "Charge Code Not Founds"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        resp = transaction_with_charge(transaction_id,get_charge_code,get_txn_obj,amount,company_id=company_id, user = request.user.pk)
                        if resp:
                            message = response_message('Success', message=f"Its Success, Transaction Id {transaction_id}",
                                                       record_id=transaction_id)
                            return Response(data=message, status=status.HTTP_201_CREATED)
                        else:
                            message = response_message('Failed',
                                                       message=f"Its Failed, Transaction Id {transaction_id}",
                                                       record_id=transaction_id)
                            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        transaction_without_charge(transaction_id, get_txn_obj, amount, company_id=company_id, user=user)
                        resp = update_custom_transaction_details(transaction_id, company_id,
                                                                 list(input_params_values.keys()),
                                                                 list(input_params_values.values()), user_id=None)
                        print('resp ',resp)
                        message = response_message('Success', message=f"Its Success, Transaction Id {transaction_id}",
                                                   record_id=transaction_id)
                        return Response(data=message, status=status.HTTP_201_CREATED)
                transaction_type_id = get_txn_obj.pk
                account_category = get_txn_obj.category_of_account.account_category_id
                print('account_category ', account_category)
                dr_obj = Accounts.objects.filter(Q(company_id=company_id) & Q(account_category_id=account_category))
                if not dr_obj.exists():
                    return Response({'message': 'Company account not found'}, status=status.HTTP_400_BAD_REQUEST)
                dr_acc = dr_obj.last().pk
                cr_obj = Accounts.objects.filter(Q(company_id=company_id) & Q(account_category__name='Income'))
                if not cr_obj.exists():
                    return Response({'message': 'Company Cashbook account not found'},
                                    status=status.HTTP_400_BAD_REQUEST)
                cr_acc = cr_obj.last().pk  # Just fixed credit account id

                logged_user_details = request.user.company_name
                local_currency_name = logged_user_details.local_currency
                local_currency_id = logged_user_details.local_currency.pk
                # commented to check teller
                # teller_profile = TellerProfile.objects.get(user=request.user)
                # is_teller = teller_profile.can_process_transaction(amount, get_txn_obj.name.lower())
                # if not is_teller[0]:
                #     return Response({'message': is_teller[1]}, status=status.HTTP_400_BAD_REQUEST)

                get_ex_rate = get_exchange_rate(str(local_currency_name), str(local_currency_name),
                                                base_currency=str(local_currency_name))
                if not get_ex_rate[0]:
                    return Response({'message': get_ex_rate[1]}, status=status.HTTP_400_BAD_REQUEST)
                res_cal_mode, ex_rate_id, ex_rate = get_ex_rate[1], get_ex_rate[2], get_ex_rate[3]
                txn_type_obj = TransactionType.objects.get(name=get_txn_obj.name)
                dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
                cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
                charge_code = get_txn_obj.charge_code.charge_code_id
                credit_amount = amount * ex_rate

                # =========== GET TRANSACTION CODE DETAILS ===============
                get_dr_txn_code_obj = get_txn_code_details(dr_txn_code)
                get_cr_txn_code_obj = get_txn_code_details(cr_txn_code)
                if get_dr_txn_code_obj is None or get_cr_txn_code_obj is None:
                    return Response(data={"message": "Transaction Code Not Not Founds"},
                                    status=status.HTTP_400_BAD_REQUEST)
                # ============= debit txn code details ======================
                get_dr_debit_gl_line , get_dr_credit_gl_line = get_dr_txn_code_obj.debit_gl_line.gl_line_id , get_dr_txn_code_obj.credit_gl_line.gl_line_id
                get_dr_overdraft_check = get_dr_txn_code_obj.overdraft_check
                # ============= credit txn code details ======================
                get_cr_debit_gl_line , get_cr_credit_gl_line = get_cr_txn_code_obj.debit_gl_line.gl_line_id , get_cr_txn_code_obj.credit_gl_line.gl_line_id
                get_cr_overdraft_check = get_cr_txn_code_obj.overdraft_check

                # ============ CHARGE CODE DETAILS ===========================
                get_charge_code = get_charge_code_details(charge_code)
                if get_charge_code is None:
                    return Response(data={"message": "Charge Code Not Founds"},
                                    status=status.HTTP_400_BAD_REQUEST)
                charge_amount , currency , gl_line_to_credit, transaction_code_to_use = get_charge_code.charge_amount , get_charge_code.currency, get_charge_code.gl_line_to_credit.gl_line_id, get_charge_code.transaction_code_to_use.transaction_code_id
                get_gl_acc_no = get_account_number(glline=gl_line_to_credit)
                gl_acc_no = get_gl_acc_no.account_id

                resp = get_exchange_rate(local_currency_name, local_currency_name)
                if not resp[0]:
                    message = {
                        "error": str(resp[1])
                    }
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                exchange_rate_calc_mode = resp[1]
                exchange_rate_used = resp[2]
                ex_rate = resp[3]
                # ================== CREATE TRANSACTION ==================
                transaction_id = generate_txn_id()
                obj = common_transaction_create(transaction_id, transaction_type_id, dr_acc, local_currency_id, amount,
                                                cr_acc, local_currency_id, amount, res_cal_mode, ex_rate_id,
                                                charges_applied=False, status='pending')
                if obj is None:
                    return Response(data={"message": "TECHNICAL ERROR WHILE CREATING TXN"},
                                    status=status.HTTP_400_BAD_REQUEST)
                # ============================== Account Entries ==========================
                entry_type = 'PL'

                resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                                     credit_currency=local_currency_id, total_debit_amt=amount,
                                     debit_currency=local_currency_id,
                                     dr_acc=dr_acc, cr_acc=cr_acc, debit_credit_marker='DebitCredit',
                                     user=request.user.pk, company=company_id)
                get_resp2 = account_entry(entry_type, transaction_id, transaction_code_to_use, transaction_code_to_use,
                                          charge_amount,
                                          credit_currency=local_currency_id,
                                          total_debit_amt=0, debit_currency=local_currency_id,
                                          dr_acc=None,
                                          cr_acc=gl_acc_no,
                                          debit_credit_marker='Credit',
                                          user=request.user.pk, company=company_id)

                # now debit transaction code and credit txn code wise wise entries
                # ========================= DR. TXN CODE =========================
                get_dr_gl_acc_no_obj = get_account_number(glline=get_dr_debit_gl_line)
                dr_gl_acc_no = get_dr_gl_acc_no_obj.account_id
                get_cr_gl_acc_no_obj = get_account_number(glline=get_dr_credit_gl_line)
                cr_gl_acc_no = get_cr_gl_acc_no_obj.account_id

                get_resp1 = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                          amount,
                                          credit_currency=local_currency_id,
                                          total_debit_amt=amount, debit_currency=local_currency_id,
                                          dr_acc=dr_gl_acc_no,
                                          cr_acc=cr_gl_acc_no,
                                          debit_credit_marker='DebitCredit',
                                          user=request.user.pk, company=company_id)

                # ========================= CR. TXN CODE =========================
                get_cr_dr_gl_acc_no_obj = get_account_number(glline=get_cr_debit_gl_line)
                cr_dr_gl_acc_no = get_cr_dr_gl_acc_no_obj.account_id
                get_cr_gl_acc_no_obj = get_account_number(glline=get_cr_credit_gl_line)
                cr_gl_acc_no = get_cr_gl_acc_no_obj.account_id
                get_resp1 = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code,
                                          amount,
                                          credit_currency=local_currency_id,
                                          total_debit_amt=amount, debit_currency=local_currency_id,
                                          dr_acc=cr_dr_gl_acc_no,
                                          cr_acc=cr_gl_acc_no,
                                          debit_credit_marker='DebitCredit',
                                          user=request.user.pk, company=company_id)


                obj.transaction_id = transaction_id
                obj.exchange_rate_calc_mode = res_cal_mode
                obj.exchange_rate_used_id = ex_rate_id
                obj.to_amount = amount
                obj.status = 'success' if resp else 'pending'
                obj.save()
                # part of teller object
                # commented
                # teller_profile.clear_teller_amount(amount, get_txn_obj.name.lower())
                # update into Custom Transaction Details tables
                resp = update_custom_transaction_details(transaction_id, company_id, list(input_params_values.keys()),
                                                         list(input_params_values.values()), user_id=None)
                print('CUSTOM TRANSACTION DETAILS UPDATE RESPONSE ', resp)
                message = response_message('Success', message=f"Its Success, Transaction Id {transaction_id}",
                                           record_id=transaction_id)
                return Response(data=message, status=status.HTTP_201_CREATED)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

def check_account_balance(account_id, amount):
    try:
        obj = Accounts.objects.filter(account_id = account_id)
        if not obj.exists():
            msg = "Invalid Account"
            return [False, msg]
        obj_first = obj.first()
        total_balance = obj_first.total_balance
        if amount > total_balance:
            msg = "Insufficient funds"
            return [False, msg]
        return [True, "Continue"]

    except Exception as error:
        return [False, f"""{error}"""]
def get_account_details(account_id):
    try:
        obj = Accounts.objects.filter(account_id = account_id)
        if not obj.exists():
            msg = "Invalid Account"
            return [False, msg]
        obj_first = obj.first()
        return [obj_first, "Continue"]

    except Exception as error:
        return [False, f"""{error}"""]




class FundsTransferAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FundsTransferSerializer

    @swagger_auto_schema(request_body=FundsTransferSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = FundsTransferSerializer(data=request.data)
            if serializer.is_valid():
                from_account_no = dr_acc = serializer.data.get('from_account_no')
                to_account_no = cr_acc = serializer.data.get('to_account_no')
                transaction_type = cr_acc = serializer.data.get('transaction_type')
                amount = serializer.data.get('amount')
                if from_account_no == to_account_no:
                    message = {"status": "Failed", "message": "From and to account numbers must be different."}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
                check_funds = check_account_balance(from_account_no, amount)
                if not check_funds[0]:
                    message = {"status": "Failed", "message": check_funds[1]}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

                # Funds Transfer
                entry_type = 'PL'
                transaction_id = generate_txn_id()
                acc_obj = get_account_details(account_id=from_account_no)
                if not acc_obj[0]:
                    message = {"status": "Failed", "message": acc_obj[1]}
                    return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
                acc_obj = acc_obj[0]
                local_currency_id = acc_obj.base_currency.pk
                txn_type_obj = TransactionType.objects.get(pk=transaction_type)
                dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
                cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
                # charge_code = get_txn_obj.charge_code.charge_code_id
                company_id = request.user.company_name.pk

                # credit_amount = amount * ex_rate

                resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                                     credit_currency=local_currency_id, total_debit_amt=amount,
                                     debit_currency=local_currency_id,
                                     dr_acc=dr_acc, cr_acc=cr_acc, debit_credit_marker='DebitCredit',
                                     user=request.user.pk, company=company_id, ref_no=None)

                message = {"status": "Success", "message": "Its Success"}
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)




class BankRegistrationAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BankRegistrationSerialize

    @swagger_auto_schema(responses={200: BankRegistrationSerialize(many=True)})
    def get(self, request, *args, **kwargs):
        try:
            records = BankRegistration.objects.all()
            serializer = BankRegistrationSerialize(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(request_body=BankRegistrationSerialize)
    def post(self, request, *args, **kwargs):
        try:
            serializer = BankRegistrationSerialize(data=request.data)
            if serializer.is_valid():
                obj = serializer.save()
                message = response_message('Success', message="Its Success", record_id=obj.pk)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class FundsTransferBankToMemberAccountAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BankToMemberAccountSerializer

    @swagger_auto_schema(request_body=BankToMemberAccountSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = BankToMemberAccountSerializer(data=request.data)
            if serializer.is_valid():
                print('itns okay')
                bank_id = serializer.data.get('bank_id')
                member_id = cr_acc = serializer.data.get('member_id')
                reference_type = cr_acc = serializer.data.get('reference_type')
                reference_id = cr_acc = serializer.data.get('reference_id')
                total_amount = cr_acc = serializer.data.get('total_amount')
                member_acc_id = cr_acc = serializer.data.get('member_acc_id')
                member_amount = cr_acc = serializer.data.get('member_amount')
                transaction_type = cr_acc = serializer.data.get('transaction_type')
                bank_account = Accounts.objects.filter(Q(bank__code=bank_id) & Q(account_category__name='Cashbook'))
                if not bank_account.exists():
                    return Response({'message': 'Company Cashbook account not found'},
                                    status=status.HTTP_400_BAD_REQUEST)
                from_account = dr_acc = bank_account.last().pk
                entry_type = 'PL'
                transaction_id = generate_txn_id()
                resp = account_entry(entry_type, transaction_id, None, None, credit_amount=0,
                                     credit_currency=None, total_debit_amt=total_amount,
                                     debit_currency=None,
                                     dr_acc=dr_acc, cr_acc=None, debit_credit_marker='Debit',
                                     user=None, company=None, ref_no=None)
                for cr_acc, amount in zip(eval(member_acc_id),eval(member_amount)):
                    acc_obj = Accounts.objects.get(account_number=cr_acc)
                    cr_acc = acc_obj.pk

                    resp = account_entry(entry_type, transaction_id, None, None, credit_amount=amount,
                                         credit_currency=None, total_debit_amt=0,
                                         debit_currency=None,
                                         dr_acc=None, cr_acc=cr_acc, debit_credit_marker='Credit',
                                         user=None, company=None, ref_no=reference_id)

                print('transaction_id ',transaction_id)
                message = {"status": "Success", "message": f"Its Success, your transaction id : {transaction_id}"}
                return Response(data=message, status=status.HTTP_201_CREATED)
            print('im here')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print('Excep block')
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)



class FundsTransferMemberToBankAccountAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BankToMemberAccountSerializer

    @swagger_auto_schema(request_body=BankToMemberAccountSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = BankToMemberAccountSerializer(data=request.data)
            if serializer.is_valid():
                print('its okay')
                bank_id = serializer.data.get('bank_id')
                member_id = cr_acc = serializer.data.get('member_id')
                reference_type = cr_acc = serializer.data.get('reference_type')
                reference_id = cr_acc = serializer.data.get('reference_id')
                total_amount = cr_acc = serializer.data.get('total_amount')
                member_acc_id = cr_acc = serializer.data.get('member_acc_id')
                member_amount = cr_acc = serializer.data.get('member_amount')
                transaction_type = cr_acc = serializer.data.get('transaction_type')
                bank_account = Accounts.objects.filter(Q(bank__code=bank_id) & Q(account_category__name='Cashbook'))
                if not bank_account.exists():
                    return Response({'message': 'Company Cashbook account not found'},
                                    status=status.HTTP_400_BAD_REQUEST)
                from_account = dr_acc = bank_account.last().pk
                entry_type = 'PL'
                transaction_id = generate_txn_id()
                resp = account_entry1(entry_type, transaction_id, None, None, credit_amount=0,
                                     credit_currency=None, total_debit_amt=total_amount,
                                     debit_currency=None,
                                     dr_acc=dr_acc, cr_acc=None, debit_credit_marker='Debit',
                                     user=None, company=None, ref_no=None)
                for cr_acc, amount in zip(eval(member_acc_id),eval(member_amount)):
                    acc_obj = Accounts.objects.get(account_number=cr_acc)
                    cr_acc = acc_obj.pk

                    resp = account_entry1(entry_type, transaction_id, None, None, credit_amount=amount,
                                         credit_currency=None, total_debit_amt=0,
                                         debit_currency=None,
                                         dr_acc=None, cr_acc=cr_acc, debit_credit_marker='Credit',
                                         user=None, company=None, ref_no=reference_id)

                print('transaction_id ',transaction_id)


                # # Funds Transfer
                # entry_type = 'PL'
                # transaction_id = generate_txn_id()
                # acc_obj = get_account_details(account_id=from_account_no)
                # if not acc_obj[0]:
                #     message = {"status": "Failed", "message": acc_obj[1]}
                #     return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
                # acc_obj = acc_obj[0]
                # local_currency_id = acc_obj.base_currency.pk
                # txn_type_obj = TransactionType.objects.get(pk=transaction_type)
                # dr_txn_code = txn_type_obj.debit_transaction_code.transaction_code_id
                # cr_txn_code = txn_type_obj.credit_transaction_code.transaction_code_id
                # # charge_code = get_txn_obj.charge_code.charge_code_id
                # company_id = request.user.company_name.pk
                #
                # # credit_amount = amount * ex_rate
                #
                # resp = account_entry(entry_type, transaction_id, dr_txn_code, cr_txn_code, credit_amount=amount,
                #                      credit_currency=local_currency_id, total_debit_amt=amount,
                #                      debit_currency=local_currency_id,
                #                      dr_acc=dr_acc, cr_acc=cr_acc, debit_credit_marker='DebitCredit',
                #                      user=request.user.pk, company=company_id, ref_no=None)

                message = {"status": "Success", "message": f"Its Success, your transaction id : {transaction_id}"}
                return Response(data=message, status=status.HTTP_201_CREATED)
            print('im here')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print('Excep block')
            message = {"status": "Failed", "message": str(error)}
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class GetCompanyAccountNumberAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GetCompanyAccountsSerializer

    @swagger_auto_schema(responses={200: GetCompanyAccountsSerializer(many=True)})
    def get(self, request, company_id, *args, **kwargs):
        try:
            # company_id = request.user.company_name.pk
            records = Accounts.objects.filter(company_id=company_id)
            serializer = GetCompanyAccountsSerializer(records, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class SignUpAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SignUpSerializer
    @swagger_auto_schema(request_body=SignUpSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = SignUpSerializer(data=request.data)
            if serializer.is_valid():
                # Manually hash the password before saving
                password = make_password(serializer.validated_data['password'])
                user_data = serializer.validated_data
                user_data['password'] = password

                # Create the user with hashed password
                obj = User.objects.create(**user_data)
                obj.is_customer = True
                com_obj = Company.objects.create(created_by=obj)  # create the company
                obj.company_name = com_obj  # update company id
                obj.save()
                data = {
                    'user_id':obj.pk,
                    'company_id':com_obj.pk
                }
                message = response_message('Success', message="Its Success", record_id=data)
                return Response(data=message, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            message = response_message('Failed', message=f"{error}")
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
