from django.shortcuts import render, redirect
from pesanile_accounting.scripts_pr import receivable_atomic
from pesanile_accounting.views_ms import post_receivable_and_payable_transaction_ms
from sub_part.models import  *
import razorpay
from pesanile_accounting.models import AccountReceivable, TransactionType as Finance_TransactionType

# Create your views here.
from django.contrib import messages
from .mpesa_payments import *
from sub_part.api_call import *
# BASE_URL = 'https://bbaccountingsms.pythonanywhere.com/'
BASE_URL='http://127.0.0.1:9000/'

# access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMxNDc3MjgxLCJpYXQiOjE3MzEzOTA4ODEsImp0aSI6IjU2YTRhZjlmMTA5NjQwYzFhZGVmMDVjZWI0MTU5YThhIiwidXNlcl9pZCI6MTQ0fQ.XOMm5Y06Qqee4-3dRjU8dYZwl4evilY_1FUOQa2qMtA"


def fees_payment(request,pk):
    print("request.session.get('user_token')",request.session.get('user_token'))
    token = request.session.get('user_token')
    print("token_payment",token)
    endpoint = 'finance/transaction-type/'
    general_setting = GeneralSetting.objects.all().last()
    payment_key=PaymentKeys.objects.all().last()
    fees_records=FeesAssign.objects.get(id=pk)
    print("fees_records",fees_records.student)
    branch_id = Branch.objects.get(id=fees_records.branch.id)
    print("branch_id",branch_id.school.reference_id)
    reference_number=fees_records
    print('reference_number',reference_number)
    balance_amount=str(fees_records.balance_amount)
    print('balance_amount',balance_amount)
    transaction_type=Finance_TransactionType.objects.get(name='Fees collection') 
    print('transaction_type',transaction_type.pk)      
    print((transaction_type.pk,reference_number,reference_number,None,balance_amount,request.user.pk))
    check = post_receivable_and_payable_transaction_ms(transaction_type.pk,reference_number,reference_number,None,balance_amount,request.user.pk)
    print('check',check)
    balance_amount=float(balance_amount)
 
    receivable_amt=AccountReceivable.objects.get(reference_number=reference_number.pk)
    receivable_amt.amount_received+=balance_amount
    receivable_amt.amount_due-=balance_amount
    receivable_amt.save()
    receivable =receivable_atomic(reference_number.pk,balance_amount)
    print('receivable',receivable)
    # endpoint = 'finance/transaction-type/'
    endpoint_transaction = 'finance/all-transaction/'
    response = call_get_method(BASE_URL, endpoint, token)
    transaction_data = response.json()
    print("transaction_data", transaction_data)

    # Extract 'name' and 'transaction_type_id' into a list of dictionaries
    transaction_list = [{'name': item['name'], 'transaction_type_id': item['transaction_type_id']} for item in transaction_data]

    print("transaction_list", transaction_list)
    if response.status_code != 200:
        return render(request, 'error500.html', {'error': str(response.json())})
    print("fees_records",fees_records.fine_amount)
    if general_setting.country == 'India':        
        name = request.user.first_name
        transaction_type=request.POST.get('transaction_type')
        print("transaction_type",transaction_type)
        student_information = {
        "student_name": f"{fees_records.student.first_name}",
            "roll_no": f"{fees_records.student.roll_number}"
        }

        # converting student_information to JSON format
        student_information_json = json.dumps(student_information)
        print("++++tudent",type(student_information_json))

        # using it in the data dictionary
        data = {
            'transaction_type_id': str(transaction_type),
            'company_id': str(branch_id.school.reference_id),
            'amount': int(fees_records.fine_amount),
            'input_params_values': student_information 
        }
        print("++++++++++++++++++",type(data))

        json_data = json.dumps(data)
        print("=========", type(json_data))

        response = call_post_method(BASE_URL, endpoint_transaction, json_data, token)
        print("response+++", response)
        if response.status_code != 200:
            print('Response Status Code:', response.content)
        response_data = json.loads(response.content.decode('utf-8')) 
        transaction_id=response_data['record_id']
        Transaction.objects.create(
            student_id=fees_records.student.id,
            reference_id=transaction_id,                   
            branch_id = branch_id.id
        )    
        amount = int(fees_records.fees.amount) * 100
        # create Razorpay client
        client = razorpay.Client(auth=(payment_key.razorpay_key_id, payment_key.razorpay_key_secret))

        # create order
        response_payment = client.order.create(dict(amount=amount, currency='INR') )

        order_id = response_payment['id']
        order_status = response_payment['status']
        return render(request, 'payment/fees_payment.html',{'transaction_list':transaction_list,'fees_records':fees_records, 'payment': response_payment,'payment_key':payment_key})
    elif general_setting.country == 'Kenya':
        if request.method=='POST':            
            number=request.POST.get('phone_number')
            transaction_type=request.POST.get('transaction_type')
            print("transaction_type+++",transaction_type)
            student_information = {
            "student_name": f"{fees_records.student.first_name}",
                "roll_no": f"{fees_records.student.roll_number}"
            }

            # converting student_information to JSON format
            student_information_json = json.dumps(student_information)
            print("++++tudent",type(student_information_json))

            # using it in the data dictionary
            data = {
                'transaction_type_id': str(transaction_type),
                'company_id': str(branch_id.school.reference_id),
                'amount': int(fees_records.fine_amount),
                'input_params_values': student_information 
            }
            print("++++++++++++++++++",type(data))

            json_data = json.dumps(data)
            print("=========", type(json_data))

            response = call_post_method(BASE_URL, endpoint_transaction, json_data, token)
            print("response+++", response)
            if response.status_code != 200:
                print('Response Status Code:', response.content)
                response_data = json.loads(response.content.decode('utf-8')) 
            transaction_id=response_data['record_id']
            Transaction.objects.create(
                student_id=fees_records.student.id,
                reference_id=transaction_id,                   
                branch_id = branch_id.id
            )
            # result = mpesa_stk_push(int(fees_records.fees.amount),number,request.user.first_name)
            # print("result===",result)
            # messages.warning(request, result['errorMessage'])
        sudent_records= StudentAdmission.objects.filter(user_parent=request.user)
        print("sudent_records+++",sudent_records)
        return render(request, 'payment/fees_payment.html',{'transaction_list':transaction_list,'fees_records':fees_records,'sudent_records':sudent_records})
    else:
        messages.warning(request, 'Payment mode')
        return redirect('fees_parent')
        
        

def payment_status(request):
    payment_key=PaymentKeys.objects.all().last()
    response = request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=(payment_key.razorpay_key_id, payment_key.razorpay_key_secret))
    print("client+++",client)
    try:
        status = client.utility.verify_payment_signature(params_dict)
        # cold_coffee = ColdCoffee.objects.get(order_id=response['razorpay_order_id'])
        # cold_coffee.razorpay_payment_id = response['razorpay_payment_id']
        # cold_coffee.paid = True
        # cold_coffee.save()
        return render(request, 'payment/payment_status.html', {'status': True})
    except:
        return render(request, 'payment/payment_status.html', {'status': False})
    
