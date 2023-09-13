import smtplib
import ssl
import os


def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    email_sender = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    email_receiver = os.getenv("EMAIL")

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as mail_server:
        mail_server.login(email_sender, password)
        mail_server.sendmail(email_sender, email_receiver, message)

