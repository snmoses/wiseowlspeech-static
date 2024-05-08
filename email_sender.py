import smtplib
from email.message import EmailMessage
import os


def send_email(name, signup_email, message):
    try:
        gmail_user = 'pretoriusfrederik@gmail.com'
        to_email = "cindymccallumslp@gmail.com"

        msg = EmailMessage()
        content = f'''New email received from:
        Name: {name}
        Email: {signup_email}
        Message: {message}
        '''

        msg.set_content(content)
        msg['Subject'] = f'''WiseOwlSpeech.com: new message from {name} - {signup_email}'''
        msg['From'] = gmail_user
        msg['To'] = to_email

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.ehlo()  # Can be omitted
        server.starttls()  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(gmail_user, 'jpbb ajoo keut urcm')
        server.send_message(msg)
        server.quit()
        return "Success"
    except:
        return "Failure"

if __name__ == "__main__":
    import sys
    name = sys.argv[1]
    signup_email = sys.argv[2]
    message = sys.argv[3]
    result = send_email(name, signup_email, message)
    print(result)
