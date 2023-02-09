import smtplib
import ssl
from email.message import EmailMessage

def gmail_send_message(to_address, from_address, subject, message_text):

    with open("../instance/pythonpass", 'r') as file:
        email_password = file.read()

    em = EmailMessage()
    em['From'] = from_address
    em['To'] = to_address
    em['Subject'] = subject
    em.set_content(message_text)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(from_address, email_password)
            smtp.sendmail(from_address, to_address, em.as_string())
        return "Email Sent!"
    except:
        return "Email failed to send"



