from sendEmail import gmail_send_message

def send_verification_email(to_address, name, code):
    subject = f"Hello There, {name}"
    message = f"<h2>Here is your verification code!</h2> <br> Verification Code: <b>{code}</b> <br> <br> Warning: This code will expire in the next 24 hours"
    gmail_send_message(to_address, "theanishcounter@gmail.com", subject, message)

if __name__ == '__main__':
    send_verification_email("theanishcounter@gmail.com", "Obi Wan Kenobi", 123456)