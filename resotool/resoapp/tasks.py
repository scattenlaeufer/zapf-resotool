from celery import shared_task
from celery.result import AsyncResult
from django.core import mail

from .models import Resolution, ResolutionEmail, SendStatus
from resotool import settings


def send_reso(reso_id, mail_text, subject, sender):
    resolution = Resolution.objects.get(pk=reso_id)
    mail_list = []
    mail_data_list = []
    for recipient in resolution.recipient_set.all():
        mail_data_list.append((subject, mail_text, sender, [str(recipient)]))
        reso_mail = ResolutionEmail(
            recipient=recipient,
            resolution=resolution,
            email_text=mail_text,
            status=SendStatus.IN_PROGRESS,
        )
        reso_mail.save()
        mail_list.append(reso_mail)
    send_results = mail.send_mass_mail(mail_data_list)

    if isinstance(send_results, list):
        for email, send_result in zip(mail_list, send_results):
            send_result.then(on_reso_sent(email), on_send_error(email))
        return send_results
    else:
        return send_results


def on_reso_sent(email):
    def return_func(result):
        email.status = SendStatus.SUCCESS if result.get() else SendStatus.FAILURE
        email.save()

    return return_func


def on_send_error(email):
    def return_func(result):
        email.status = SendStatus.FAILURE
        email.save()

    return return_func
