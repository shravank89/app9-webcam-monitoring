import glob
import smtplib
import ssl
import os
from email.message import EmailMessage
import imghdr
import glob


def clean_folder():
    images = glob.glob("images/*.png")
    for image in images:
        os.remove(image)


def send_email(image_path):
    host = "smtp.gmail.com"
    port = 465
    email_sender = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    email_receiver = os.getenv("EMAIL")

    context = ssl.create_default_context()

    email_message = EmailMessage()
    email_message["Subject"] = "New Customer Showed up!"
    email_message.set_content(" Hey New customer arrived, just check it out!")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    with smtplib.SMTP_SSL(host, port, context=context) as mail_server:
        mail_server.login(email_sender, password)
        mail_server.sendmail(email_sender, email_receiver, email_message.as_string())

