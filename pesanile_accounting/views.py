from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import (
    AccountType, AccountCategory, Accounts, AccountHolder, GLLine,
    AssetType, TransactionCode, ChargeCode, TransactionType,
    Transaction, TransactionDetail, Reconciliation, ServicePayment
)
from .serializers import  ServicePaymentSerializer, MyTokenObtainPairSerializer
from .scripts import *
from .account_entries import *
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



# #
class ServicePaymentAPIView(APIView):
    serializer_class = ServicePaymentSerializer

    @swagger_auto_schema(request_body=ServicePaymentSerializer)
    def post(self, request):
        try:
            serializer = ServicePaymentSerializer(data=request.data)
            if serializer.is_valid():
                # serializer.save()
                user = serializer.data.get('user')
                account_holder = serializer.data.get('debit_acc_number')
                credit_acc_number_holder_id = serializer.data.get('credit_acc_number')
                transaction_type = serializer.data.get('transaction_type')
                amount = total_amount = from_amount = to_amount = serializer.data.get('amount')
                # ========== SERVICE PAYMENT =============
                print('user: ', user)
                print('account_holder: ', account_holder)
                print('transaction_type: ', transaction_type)
                print('amount: ', amount)
                get_acc_holder_number_obj = get_account_number(
                    acc_holder_id=account_holder)
                get_acc_holder_number_obj_cr = get_account_number(
                    acc_holder_id=credit_acc_number_holder_id)
                if get_acc_holder_number_obj is None or get_acc_holder_number_obj_cr is None:
                    return Response(data={"message": "Account Holder Account Not Founds"},
                                    status=status.HTTP_400_BAD_REQUEST)
                print('get_acc_holder_number_obj ', get_acc_holder_number_obj)
                from_account_id = get_acc_holder_number_obj.account_id
                from_currency_name = get_acc_holder_number_obj.base_currency
                from_currency_id = get_acc_holder_number_obj.base_currency.currency_id
                to_account_id = get_acc_holder_number_obj_cr.account_id
                to_currency_name = get_acc_holder_number_obj_cr.base_currency
                to_currency_id = get_acc_holder_number_obj_cr.base_currency.currency_id
                # get txn type details transaction_code_id
                print('its okay...')
                get_txn_obj = get_txn_type_details(transaction_type)
                if get_txn_obj is None:
                    return Response(data={"message": "Transaction Type Not Founds"},
                                    status=status.HTTP_400_BAD_REQUEST)
                debit_transaction_code = get_txn_obj.debit_transaction_code.transaction_code_id
                credit_transaction_code = get_txn_obj.credit_transaction_code.transaction_code_id
                charge_code = get_txn_obj.charge_code.charge_code_id
                print('its okay too')

                # =========== GET TRANSACTION CODE DETAILS ===============
                get_dr_txn_code_obj = get_txn_code_details(debit_transaction_code)
                get_cr_txn_code_obj = get_txn_code_details(credit_transaction_code)
                if get_dr_txn_code_obj is None or get_cr_txn_code_obj is None:
                    return Response(data={"message": "Transaction Code Not Not Founds"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # ============= debit txn code details ======================
                get_dr_debit_gl_line = get_dr_txn_code_obj.debit_gl_line.gl_line_id
                get_dr_credit_gl_line = get_dr_txn_code_obj.credit_gl_line.gl_line_id
                get_dr_overdraft_check = get_dr_txn_code_obj.overdraft_check
                # ============= credit txn code details ======================
                get_cr_debit_gl_line = get_cr_txn_code_obj.debit_gl_line.gl_line_id
                get_cr_credit_gl_line = get_cr_txn_code_obj.credit_gl_line.gl_line_id
                get_cr_overdraft_check = get_cr_txn_code_obj.overdraft_check
                # ============ CHARGE CODE DETAILS ===========================
                print('its okay 3')
                get_charge_code = get_charge_code_details(charge_code)
                if get_charge_code is None:
                    return Response(data={"message": "Charge Code Not Founds"},
                                    status=status.HTTP_400_BAD_REQUEST)
                charge_amount = get_charge_code.charge_amount
                currency = get_charge_code.currency
                print('okay noewhere')
                gl_line_to_credit = get_charge_code.gl_line_to_credit.gl_line_id
                get_gl_acc_no = get_account_number(glline=gl_line_to_credit)
                print('get_gl_acc_no ',get_gl_acc_no)
                gl_acc_no = get_gl_acc_no.account_id
                transaction_code_to_use = get_charge_code.transaction_code_to_use.transaction_code_id
                print('its okay good')
                # ======================== Entries =============================
                transaction_id = generate_txn_id()

                details_payload = {
                    'get_acc_holder_number': get_acc_holder_number_obj.account_id,
                    'amount': amount,
                    'get_dr_debit_gl_line': get_dr_debit_gl_line,
                    'get_dr_credit_gl_line': get_dr_credit_gl_line,
                    'get_dr_overdraft_check': get_dr_overdraft_check,
                    'get_cr_debit_gl_line': get_cr_debit_gl_line,
                    'get_cr_credit_gl_line': get_cr_credit_gl_line,
                    'get_cr_overdraft_check': get_cr_overdraft_check,
                    'charge_amount': charge_amount,
                    'currency': 'KSH',
                    'gl_line_to_credit': gl_line_to_credit,
                    'transaction_code_to_use': transaction_code_to_use,
                    'transaction_id': transaction_id,
                }
                resp = get_exchange_rate(from_currency_name, to_currency_name)
                if not resp[0]:
                    message = {
                        "error": str(resp[1])
                    }
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
                print('resp ', resp)
                exchange_rate_calc_mode = resp[1]
                exchange_rate_used = resp[2]
                ex_rate = resp[3]
                # ================== CREATE TRANSACTION ==================
                txn_resp_or_obj = common_transaction_create(transaction_id, transaction_type, from_account_id,
                                                     from_currency_id, from_amount, to_account_id, to_currency_id,
                                                     to_amount, exchange_rate_calc_mode, exchange_rate_used,
                                                     charges_applied=False, status='pending')
                if txn_resp_or_obj is None:
                    return Response(data={"message": "TECHNICAL ERROR WHILE CREATING TXN"},
                                    status=status.HTTP_400_BAD_REQUEST)
                # ============================== Account Entries ==========================
                entry_type = 'AL'
                amount = amount - charge_amount
                # get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code,
                #                           credit_transaction_code, amount, total_debit_amt=total_amount,
                #                           currency=from_currency_id,
                #                           dr_acc=from_account_id, cr_acc=to_account_id,
                #                           debit_credit_marker='DebitCredit', user=None)
                get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code, credit_transaction_code, amount, credit_currency=from_currency_id,
                              total_debit_amt=total_amount, debit_currency=from_currency_id,
                              dr_acc=from_account_id,
                              cr_acc=to_account_id,
                              debit_credit_marker='DebitCredit', user=None)
                # get_resp2 = account_entry(entry_type, transaction_id, transaction_code_to_use,
                #                           transaction_code_to_use, charge_amount,
                #                           currency=to_currency_id,
                #                           dr_acc=None, cr_acc=gl_acc_no,
                #                           debit_credit_marker='Credit', user=None)

                get_resp2 = account_entry(entry_type, transaction_id, transaction_code_to_use, transaction_code_to_use, charge_amount,
                                          credit_currency=from_currency_id,
                                          total_debit_amt=0, debit_currency=to_currency_id,
                                          dr_acc=None,
                                          cr_acc=gl_acc_no,
                                          debit_credit_marker='Credit', user=None)

                # now debit transaction code and credit txn code wise wise entries
                # ========================= DR. TXN CODE =========================
                get_dr_gl_acc_no_obj = get_account_number(glline=get_dr_debit_gl_line)
                dr_gl_acc_no = get_dr_gl_acc_no_obj.account_id
                get_cr_gl_acc_no_obj = get_account_number(glline=get_dr_credit_gl_line)
                cr_gl_acc_no = get_cr_gl_acc_no_obj.account_id
                # get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code,
                #                           credit_transaction_code, total_amount, total_debit_amt=total_amount,
                #                           currency=from_currency_id,
                #                           dr_acc=dr_gl_acc_no, cr_acc=cr_gl_acc_no,
                #                           debit_credit_marker='DebitCredit', user=None)
                get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code, credit_transaction_code, total_amount,
                                          credit_currency=from_currency_id,
                                          total_debit_amt=total_amount, debit_currency=to_currency_id,
                                          dr_acc=dr_gl_acc_no,
                                          cr_acc=cr_gl_acc_no,
                                          debit_credit_marker='DebitCredit', user=None)
                print('DR TXN code ', get_resp1)
                # ========================= CR. TXN CODE =========================
                get_cr_dr_gl_acc_no_obj = get_account_number(glline=get_cr_debit_gl_line)
                cr_dr_gl_acc_no = get_cr_dr_gl_acc_no_obj.account_id
                get_cr_gl_acc_no_obj = get_account_number(glline=get_cr_credit_gl_line)
                cr_gl_acc_no = get_cr_gl_acc_no_obj.account_id
                # get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code,
                #                           credit_transaction_code, total_amount, total_debit_amt=total_amount,
                #                           currency=from_currency_id,
                #                           dr_acc=cr_dr_gl_acc_no, cr_acc=cr_gl_acc_no,
                #                           debit_credit_marker='DebitCredit', user=None)

                get_resp1 = account_entry(entry_type, transaction_id, debit_transaction_code, credit_transaction_code,
                                          total_amount,
                                          credit_currency=from_currency_id,
                                          total_debit_amt=total_amount, debit_currency=to_currency_id,
                                          dr_acc=dr_gl_acc_no,
                                          cr_acc=cr_gl_acc_no,
                                          debit_credit_marker='DebitCredit', user=None)

                print('CR TXN code ', get_resp1)
                print('Serializers Data: ', serializer.data)
                # update the txn update that txn happened successfully
                txn_resp_or_obj.status = 'success'
                txn_resp_or_obj.save()

                return Response(details_payload, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
