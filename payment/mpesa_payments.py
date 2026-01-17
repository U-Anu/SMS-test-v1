import base64
import json
from datetime import datetime

import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from payment.models import PaymentKeys
# from .models import MpesaSTKPushPayment, MpesaC2BPayment, MpesaB2CPayment


def get_daraja_access_token(consumer_key, consumer_secret):
    """
    Requests an access token from the Daraja API
    """
    API_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(API_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    response = response.json()
    print('get_daraja_access_token',response)
    return response["access_token"]


def get_daraja_password(business_short_code, passkey, timetamp):
    daraja_password = base64.b64encode(
        (business_short_code + passkey + timetamp).encode("ascii")
    ).decode("utf-8")
    print('get_daraja_password',daraja_password)
    return daraja_password


def stk_push_query(business_short_code, checkout_request_ID, passkey, timestamp):
    """
    Used to check the STK PUSH transaction status
    """
    API_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"

    data = {
        "BusinessShortCode": business_short_code,
        "Password": get_daraja_password(business_short_code, passkey, timestamp),
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_ID,
    }

    # headers = {
    #     "Authorization": f"Bearer {get_daraja_access_token('iWGQXFs0HLAs9t34dFhL4Z7TuaCvhGIo', 'AMXeM7nsftU2kRvA')}",
    #     "Content-Type": "application/json",
    # }
    # This is old one
    headers = {
        "Authorization": f"Bearer {get_daraja_access_token('Ahpaf90jFU6cfHhzA9TtVPCjuFcoIJsI', '4wJLMGvLpxuuEnwk')}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response = response.json()
    print()
    return response


def mpesa_stk_push(amount, phone_number, trans_description):
    """
    Send an STK PUSH to the customers phone
    """
    payment_key=PaymentKeys.objects.all().last()
    API_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    BusinessShortCode = "174379"
    Passkey = payment_key.mpesa_passkey
    Timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    Password = get_daraja_password(BusinessShortCode, Passkey, Timestamp)
    data = {
        "BusinessShortCode": BusinessShortCode,
        "Timestamp": Timestamp,
        "Password": Password,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": f'254{phone_number}',
        "PartyB": BusinessShortCode,
        "PhoneNumber": f'254{phone_number}',
        "CallBackURL": "http://127.0.0.1:8000/parent/fees_parent",
        "AccountReference": "E-PAYMENTS",
        "TransactionDesc": trans_description,
    }
    access_token = get_daraja_access_token(
        payment_key.mpesa_consumer_key, payment_key.mpesa_consumer_secret
    )
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(url=API_URL, json=data, headers=headers)
    
    print('mpesa_stk_push ', response)
    return response.json()


def check_daraja_stk_payment_status(CheckoutRequestID):
    API_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query"

    BusinessShortCode = "174379"
    Passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    Timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    Password = get_daraja_password(BusinessShortCode, Passkey, Timestamp)

    data = {
        "BusinessShortCode": BusinessShortCode,
        "Timestamp": Timestamp,
        "Password": Password,
        "CheckoutRequestID": CheckoutRequestID,
    }

    headers = {
        "Authorization": f"Bearer {get_daraja_access_token('Ahpaf90jFU6cfHhzA9TtVPCjuFcoIJsI', '4wJLMGvLpxuuEnwk')}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, json=data, headers=headers)
    return response.json()


@csrf_exempt
def mpesa_stk_push_confirmation(request):
    """
    Saves the STK PUSH transaction details to the db if the request was successful
    """

    mpesa_body = request.body.decode("utf-8")
    mpesa_payment = json.loads(mpesa_body)

    if mpesa_payment["Body"]["stkCallback"]["ResultCode"] == 0:
        stk_receipt = MpesaSTKPushPayment(
            merchantRequestID=mpesa_payment["Body"]["stkCallback"]["MerchantRequestID"],
            checkoutRequestID=mpesa_payment["Body"]["stkCallback"]["CheckoutRequestID"],
            resultDesc=mpesa_payment["Body"]["stkCallback"]["ResultDesc"],
            amount=mpesa_payment["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0][
                "Value"
            ],
            mpesaReceiptNumber=mpesa_payment["Body"]["stkCallback"]["CallbackMetadata"][
                "Item"
            ][1]["Value"],
            transactionDate=mpesa_payment["Body"]["stkCallback"]["CallbackMetadata"][
                "Item"
            ][3]["Value"],
            phoneNumber=mpesa_payment["Body"]["stkCallback"]["CallbackMetadata"][
                "Item"
            ][4]["Value"],
        )

        stk_receipt.save()

        service_paid = MainServiceTable.objects.get(
            MerchantRequestID=mpesa_payment["Body"]["stkCallback"]["MerchantRequestID"])
        service_paid.payment_status = True
        service_paid.save()

    elif (
            mpesa_payment["Body"]["stkCallback"]["ResultCode"] == 1
            or mpesa_payment["Body"]["stkCallback"]["ResultCode"] == 1032
            or mpesa_payment["Body"]["stkCallback"]["ResultCode"] == 1037
            or mpesa_payment["Body"]["stkCallback"]["ResultCode"] == 2001
    ):
        print(mpesa_payment["Body"]["stkCallback"]["ResultDesc"])

    return redirect("dashboard")


# DARAJA C2B
def register_c2b_urls(request):
    """
    Register validationURL and callbackURL for C2B transactions. This is where the confirmation/validation message is sent to if a payment succeeds or fails
    """

    if request.method == "POST":
        business_shortcode = request.POST.get("shortcode")
        confirmation_url = request.POST.get("confirmation_url")
        validation_url = request.POST.get("validation_url")

        API_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
        headers = {
            "Authorization": f"Bearer {get_daraja_access_token('xZLY2SQlljdAPUjo4jL3AY3COqcKgMaA', 'myLTOPShNT3GYOQM')}",
            "Content-Type": "application/json",
        }
        data = {
            "ShortCode": business_shortcode,
            "ResponseType": "Completed",
            "ConfirmationURL": confirmation_url,
            "ValidationURL": validation_url,
        }

        response = requests.post(API_URL, json=data, headers=headers)
        response = response.json()

        if response.get("errorMessage") != None:
            return render(
                request,
                "register_c2b_response.html",
                {"data": response["errorMessage"]},
            )
        else:
            return render(
                request,
                "register_c2b_response.html",
                {"data": response["ResponseDescription"]},
            )
    return render(request, "register_c2b_urls.html")


def daraja_c2b(request):
    """
    Used to SIMULATE a C2B transaction
    """

    API_URL = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    business_shortcode = "600989"
    amount = "1"

    data = {
        "ShortCode": business_shortcode,
        "CommandID": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "Msisdn": "254718471455",
        "BillRefNumber": "null",
    }

    # headers = {
    #     "Authorization": f"Bearer {get_daraja_access_token('fbThHU0sjIZmZ2Eg3ghlGUWeJYG9n8Rb', 'tDZTuVFUC5EvRcBp')}",
    #     "Content-Type": "application/json",
    # }

    # DARAJA APIS OLD ONE
    headers = {
        "Authorization": f"Bearer {get_daraja_access_token('xZLY2SQlljdAPUjo4jL3AY3COqcKgMaA', 'myLTOPShNT3GYOQM')}",
        "Content-Type": "application/json",
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response = response.json()
    context = {"response": response, "shortcode": business_shortcode, "amount": amount}
    return render(request, "paywithdarajac2b.html", context)


def daraja_c2b_validation(request):
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return JsonResponse(dict(context))


def daraja_c2b_confirmation(request):
    mpesa_body = request.body.decode("utf-8")
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaC2BPayment(
        first_name=mpesa_payment["FirstName"],
        last_name=mpesa_payment["LastName"],
        middle_name=mpesa_payment["MiddleName"],
        description=mpesa_payment["TransID"],
        phone_number=mpesa_payment["MSISDN"],
        amount=mpesa_payment["TransAmount"],
        reference=mpesa_payment["BillRefNumber"],
        organization_balance=mpesa_payment["OrgAccountBalance"],
        transaction_type=mpesa_payment["TransactionType"],
    )
    payment.save()

    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return JsonResponse(dict(context))


def daraja_b2c(request):
    if request.method == "POST":
        API_URL = "https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest"

        commandID = request.POST.get("commandID")
        partyB = request.POST.get("partyB").replace("+", "").replace(" ", "")
        amount = request.POST.get("amount")
        remarks = request.POST.get("remarks")
        occasion = request.POST.get("ocassion")

        data = {
            "InitiatorName": "testapi",
            "SecurityCredential": "a4yMViNOKWPBVcYAKDPRRltYeiZi6uNPoRJqG5Gja6OWM8yH8upQ85O9zy/9aJwtxOulJGFUglegwrLTWrgv0XNOym2bGt9P4A2+6Hc+8W5EwwfSrk/s74rgfd5/A/x0Y1ZZLPoGpDeK2iBIezAV+YsbFkb1inNrLyPotxf9sFsru9CcLuKW+61ydlSaetZmzmyEroGvl/YUPFB/43S3OCWsZqVhVdc57T4DxlsgOyCiMZ4xFYXcL8elsNcCGpnWj1ABHRyl8G+3Rz3SKa67UPyXKi3AWEzwKkw2/mCjd1pkR6JtfAqK0BDQ0zPB2kfVZJr9TGdStWVwVZz8x9x4Ew==",
            "CommandID": commandID,
            "Amount": amount,
            "PartyA": 600997,
            "PartyB": partyB,
            "Remarks": remarks,
            "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
            "ResultURL": "https://df6e-41-212-118-184.ap.ngrok.io/",
            "Occassion": occasion,
        }

        headers = {
            "Authorization": f"Bearer {get_daraja_access_token('xZLY2SQlljdAPUjo4jL3AY3COqcKgMaA', 'myLTOPShNT3GYOQM')}",
            "Content-Type": "application/json",
        }

        response = requests.post(API_URL, json=data, headers=headers)
        response = response.json()

        if response.get("ResponseCode") != None:
            return render(
                request,
                "daraja_b2c_result.html",
                {"data": response["ResponseDescription"]},
            )
        elif response.get("errorCode") != None:
            return render(
                request, "daraja_b2c_result.html", {"data": response["errorMessage"]}
            )
        else:
            return render(
                request,
                "daraja_b2c_form.html",
                {"data": "Something went wrong. Try again"},
            )

    return render(request, "daraja_b2c_form.html")


def daraja_b2c_resultURL_callback(request):
    mpesa_body = request.body.decode("utf-8")
    mpesa_payment = json.loads(mpesa_body)

    if mpesa_payment["Result"]["ResultCode"] == 0:

        b2c_payment = MpesaB2CPayment(
            conversationId=mpesa_payment["Result"]["ConversationId"],
            originatorConversationId=mpesa_payment["Result"][
                "OriginatorConversationId"
            ],
            resultDesc=mpesa_payment["Result"]["ResultDesc"],
            resultType=mpesa_payment["Result"]["ResultType"],
            resultCode=mpesa_payment["Result"]["ResultCode"],
            transactionID=mpesa_payment["Result"]["TransactionID"],
            transactionReceipt=mpesa_payment["Result"]["ResultParameters"][
                "ResultParameter"
            ]["TransactionReceipt"],
            transactionAmount=mpesa_payment["Result"]["ResultParameters"][
                "ResultParameter"
            ]["TransactionAmount"],
            transactionCompletedDateTime=mpesa_payment["Result"]["ResultParameters"][
                "ResultParameter"
            ]["TransactionCompletedDateTime"],
            receiverPartyPublicName=mpesa_payment["Result"]["ResultParameters"][
                "ResultParameter"
            ]["ReceiverPartyPublicName"],
        )

        b2c_payment.save()
    else:
        return None

def daraja_mpesa_reversal(request):
    if request.method == "POST":
        API_URL = "https://sandbox.safaricom.co.ke/mpesa/reversal/v1/request"

        shortcode = request.POST.get("shortcode")
        transaction_id = request.POST.get("transaction_id")
        occasion = request.POST.get("occasion")
        remarks = request.POST.get("remarks")

        data = {
            "CommandID": "TransactionReversal",
            "ReceiverParty": shortcode,
            "ReceiverIdentifierType": 4,
            "Initiator": "testapi",
            "SecurityCredential": "EdMC0w0Ym+JDfyG/PjweSSPAxn9HsoxHBmMlMO3Gy3WiQvVca/X0Pkzf5mqi6gEmVLKRKUXfHNOGXkh0kydKE7z9/TDcx5zMv9c1FkEmIX8gTtTh8VTkm089BBxnnGUQOPaDNteNUP4SznRE7mbu44+X83qcouXNS5UupxktIoOGJUa8WMRwMB62YFmReqUrrd6Hl654h9RPWIk4rqENjCT9V/voAVR4HpLJxE6RFFyaSFk0LoMIu5YtTGkzKj2caqOQQOCLWKfLjljBvMFfIdF7rZiQEeRBvZ5HXTNE6I79kLtjw7JC7d9C8cPHfTj5WdkIieL7mx1Jcr52groWHg==",
            "TransactionID": transaction_id,
            "QueueTimeOutURL": "https://rudihapa.com/timeout/",
            "ResultURL": "https://df6e-41-212-118-184.ap.ngrok.io/",
            "Remarks": remarks,
            "Occasion": occasion,
        }

        headers = {
            "Authorization": f"Bearer {get_daraja_access_token('xZLY2SQlljdAPUjo4jL3AY3COqcKgMaA', 'myLTOPShNT3GYOQM')}",
            "Content-Type": "application/json",
        }

        response = requests.post(API_URL, json=data, headers=headers)
        response = response.json()

        if response.get("errorMessage"):
            return render(
                request,
                "daraja_reversal_result.html",
                {"data": response["errorMessage"]},
            )
        else:
            return render(
                request,
                "daraja_reversal_result.html",
                {"data": response["ResponseDescription"]},
            )

    return render(request, "daraja_reversal.html")
