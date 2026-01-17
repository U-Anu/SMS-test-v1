from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from sub_part.models import EmailSetting
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def new_staff_account_email(recipient_name, to_email, staff_password):

    subject = 'Account Created Successfully'
    message = f"""
        Hi { recipient_name},

        Your school management system account has been created successfully. Use the following credentials to_email login: \n

        Username: {to_email}
        Password: {staff_password}

        Best regards,
        Your School Management Team
    """
    sender=EmailSetting.objects.first()

    smtp_server = sender.email_host
    smtp_port = sender.email_port
    auth_user = sender.gmail
    auth_password = sender.password

    try:
        msg = MIMEMultipart()
        msg['From'] = sender.gmail
        msg['To'] = to_email
        msg['Subject'] = subject

        body = message
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(auth_user, auth_password)
        text = msg.as_string()
        server.sendmail(sender.gmail, to_email, text)
        server.quit()

        success_message = "Email sent successfully!"
        print('success_message',success_message)
    except Exception as e:
        print('success_message',e)
        error_message = "Error sending email: " + str(e)




def send_email_notification(subject, message, list_mail, attachment=None):
    sender=EmailSetting.objects.first()
    smtp_server = sender.email_host
    smtp_port = sender.email_port
    auth_user = sender.gmail
    auth_password = sender.password

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(auth_user, auth_password)
        for to_email in list_mail:
            msg = MIMEMultipart()
            msg['From'] = sender.gmail
            msg['To'] = to_email
            msg['Subject'] = subject

            body = message
            msg.attach(MIMEText(body, 'plain'))

            if attachment:
                for attachment in attachment:
                    attached_file = MIMEApplication(attachment.read(), _subtype="pdf")
                    attached_file.add_header('content-disposition', 'attachment', filename=attachment.name)
                    msg.attach(attached_file)
            text = msg.as_string()
            server.sendmail(sender.gmail, to_email, text)
        print('to_email',to_email)
        server.quit()

        success_message = "Email sent successfully!"
        print('success_message',success_message)
    except Exception as e:
        print('Error_message',e)
        error_message = "Error sending email: " + str(e)



def send_email_notification1(subject, message, list_mail, attachments=None):
    sender = EmailSetting.objects.first()
    smtp_server = sender.email_host
    smtp_port = sender.email_port
    auth_user = sender.gmail
    auth_password = sender.password

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(auth_user, auth_password)

        for to_email in list_mail:
            msg = MIMEMultipart()
            msg['From'] = sender.gmail
            msg['To'] = to_email
            msg['Subject'] = subject

            # Attach the message body
            msg.attach(MIMEText(message, 'plain'))

            # Attach files if any
            if attachments:
                for attachment in attachments:
                    # If attachment is a file object
                    if hasattr(attachment, 'read'):
                        attached_file = MIMEApplication(attachment.read(), _subtype="pdf")
                        attached_file.add_header('content-disposition', 'attachment', filename=attachment.name)
                        msg.attach(attached_file)
                    # If attachment is a bytes object
                    else:
                        attached_file = MIMEApplication(attachment, _subtype="pdf")
                        attached_file.add_header('content-disposition', 'attachment', filename="attachment.pdf")
                        msg.attach(attached_file)

            # Convert the message to a string and send it
            text = msg.as_string()
            server.sendmail(sender.gmail, to_email, text)
        
        print('Email sent to:', to_email)
        server.quit()

        success_message = "Email sent successfully!"
        print(success_message)
    except Exception as e:
        error_message = "Error sending email: " + str(e)
        print('Error_message:', error_message)

