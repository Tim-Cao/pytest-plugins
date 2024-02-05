import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = "smtp.qq.com"
port = 465


def send_email(content, sender_auth_code, sender_email, subject, receiver_email):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    body = MIMEText(content, "html", "utf-8")
    msg.attach(body)

    try:
        smtp_obj = smtplib.SMTP_SSL(smtp_server, port)
        smtp_obj.login(sender_email, sender_auth_code)
        smtp_obj.sendmail(sender_email, receiver_email, msg.as_string())
        smtp_obj.quit()

        print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(e)
    except Exception as e:
        print(e)
