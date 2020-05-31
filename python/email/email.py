from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template

import smtplib


def send_email():
    """

    :return:
    """
    email_client = smtplib.SMTP("email_service")

    with open("email_template.txt") as f:
        file = f.read()
        email_template = Template(file)
        email_body = email_template.substitute(USER="Ironman", HTML_ROWS="")
        message = MIMEMultipart()
        message["From"] = "sender_email"
        message["To"] = "receiver_email"
        message["Bcc"] = ""
        message["Subject"] = "Hello World"
        message.attach(MIMEText(email_body, "html"))
        response = email_client.send_message(message)


