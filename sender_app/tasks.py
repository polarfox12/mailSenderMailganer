import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from mailSender1.celery_app import app
from sender_app.models import Clients


@app.task
def send_mail_birthday(client_id):
    client = Clients.objects.get(pk=client_id)
    subject = 'Today is your Birthday!'
    from_email = 'ksorokin88@mail.ru'
    to = client.email
    html_message = render_to_string('sender_app/mailTemplate/birthdayTemplate.html', {'name': client.name})
    plain_message = strip_tags(html_message)
    msg = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
    return 'message send to {}'.format(client.email)


# TASKS_FOR_SCHEDULER
@app.task
def send_mail_schedule():
    subject = 'Mail for test scheduler'
    from_email = os.environ['EMAIL_SMTPBOX']
    to = 'input_address'
    html_message = render_to_string('sender_app/mailTemplate/schedulerTemplate.html', {})
    plain_message = strip_tags(html_message)
    msg = EmailMultiAlternatives(subject, plain_message, from_email, [to])
    msg.attach_alternative(html_message, "text/html")
    msg.send()
