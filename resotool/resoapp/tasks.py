"""
A set of tasks to be used by resotool.
"""

from django.core import mail

from .models import Resolution, ResolutionEmail, SendStatus


def send_reso(reso_id, mail_text, subject, sender):
    """
    Send a resolution via email to all recipients. This uses the defined email
    back end from Django

    :param reso_id int: ID of the to be sent resolution
    :param mail_text str: Text for all to be sent emails
    :param subject str: Subject for all to be sent emails
    :param sender str: Email address to be used as sender
    """
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
    """
    Closure to set send status of ResolutionEmail objects on successful Celery
    task completion.
    """

    def return_func(result):
        email.status = SendStatus.SUCCESS if result.get() else SendStatus.FAILURE
        email.save()

    return return_func


def on_send_error(email):
    """
    Closure to set send status of ResolutionEmail objects on failed Celery task
    completion.
    """

    def return_func(_):
        email.status = SendStatus.FAILURE
        email.save()

    return return_func
