import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from celery import Celery

app = Celery("reso_mail", backend="rpc://", broker="pyamqp://")

app.conf.update(result_expires=3600)


@app.task
def send_mail(
    server,
    port,
    user,
    password,
    sender,
    recipient,
    subject,
    text,
    attachments=None,
    callback=None,
):
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))

    with smtplib.SMTP(host=server, port=port) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(user, password)
        smtp.send_message(msg)
        smtp.quit()
    return True
