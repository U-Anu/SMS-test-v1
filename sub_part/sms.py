from twilio.rest import Client
from sub_part.models import SMSSetting


def send_sms_notification(title,messages,to_number):
    sms_obj=SMSSetting.objects.first()
    if sms_obj:
        if sms_obj.status == 'Twilio':
            for data in to_number:
                print('===',data)
                account_sid = sms_obj.twilio_account_SID
                auth_token = sms_obj.twilio_auth_token
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                        body=f'{title} \n {messages}',
                        from_='+16083446353',
                        to='+918124003699'
                    )
                print(message.sid)
    