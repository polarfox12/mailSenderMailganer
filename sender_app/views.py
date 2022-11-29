# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import json
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ClientCreateForm
from .models import Clients
import datetime
from .tasks import send_mail_birthday


# внести информацию в БД о новом клиенте
def add_new_client(request):
    if request.method == 'POST':
        form = ClientCreateForm(request.POST)
        try:
            if form.is_valid():
                client = form.save()
                client.save()
                form = ClientCreateForm()
                return render(request, 'sender_app/clientTemplate/clientIsCreated.html', {'form': form})
        except Exception as e:
            print e
            form = ClientCreateForm()
            redirect('127.0.01:8000/')  # render(request, 'sender_app/clientTemplate/formError.html', {'form': form})
    else:
        form = ClientCreateForm()
        return render(request, 'sender_app/clientTemplate/addClientFormTemplate.html', {'form': form})


#отправить поздравление с Днем Рождения
def send_birthday(request):
    if request.method == 'GET':
        today = datetime.date.today()
        clients = Clients.objects.filter(birth__month=today.month, birth__day=today.day)
        print clients
        for client in clients:
            subject = 'Today is your Birthday!'
            from_email = 'ksorokin88@mail.ru'
            print client
            print client.email
            to = client.email
            html_message = render_to_string('sender_app/mailTemplate/birthdayTemplate.html', {'name': client.name})
            plain_message = strip_tags(html_message)
            msg = EmailMultiAlternatives(subject, plain_message, from_email, [to])
            msg.attach_alternative(html_message, "text/html")
            msg.send()
            print 'message sended!'
        return render(request, 'sender_app/clientTemplate/sendingDone.html', {})


# отправить поздравления с Днем Рождения (Celery)
def send_birthday_async(request):
    if request.method == 'GET':
        today = datetime.date.today()
        clients = Clients.objects.filter(birth__month=today.month, birth__day=today.day)
        print clients
        for client in clients:
            send_mail_birthday.delay(client.id)
            print 'message sended!'
        return render(request, 'sender_app/clientTemplate/sendingDone.html', {})


# мониторинг открытия писем
def email_seen(request, key):
    META = {header: value for header, value in request.META.items() if header.startswith(("HTTP_", "REMOTE_"))}
    Clients.objects.filter(key=key, seen_at=None).update(request=json.dumps(META), seen_at=datetime.datetime.now())
    print 'Surccessfully tracketd'
    with open(os.path.dirname(os.path.abspath(__file__)) + "res/1x1.png", "rb") as f:
        return HttpResponse(f.read(), content_type="image/png")
