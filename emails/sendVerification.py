from emails.sendEmail import gmail_send_message

def send_verification_email(to_address, name, code):
    subject = f"Hello There, {name}"

    try:
        with open("instance/website_url", "r") as file1:
            url = file1.read()
            message = f"<h2>You can verify using the following link or token</h2> <br> Verification Code: <b>{code}</b> <br> <a href='{url}/verify-email-link/{code}'>Verification Link</a><br> Warning: This code will expire in the next 24 hours"
    except:
        message = f"<h2>You can verify using the following token</h2> <br> Verification Code: <b>{code}</b> <br> Warning: This code will expire in the next 24 hours"

    try:
        gmail_send_message(to_address, "theanishcounter@gmail.com", subject, message)
    except:
        print("Failed to send email")
        pass

def send_password_reset(to_address, name, code):
    subject = f"Hello There, {name}"

    try:
        with open("instance/website_url", "r") as file1:
            url = file1.read()
            message = f"<h2>You can reset password using the following link or token</h2> <br> Verification Code: <b>{code}</b> <br> <a href='{url}/reset-password-link/{code}'>Reset Password Link</a><br> Warning: This code will expire in the next 24 hours"
    except:
        message = f"<h2>You can reset password using the following token</h2> <br> Verification Code: <b>{code}</b> <br> Warning: This code will expire in the next 24 hours"

    try:
        gmail_send_message(to_address, "theanishcounter@gmail.com", subject, message)
    except:
        print("Failed to send email")
        pass

if __name__ == '__main__':
    send_verification_email("theanishcounter@gmail.com", "Obi Wan Kenobi", 123456)