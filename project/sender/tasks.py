import json
import time

import requests
from django.db.models import Q

from fabrique.celery import app
from fabrique.settings import PROBE_SERVER_URL, TOKEN
from sender.models import Customer, Maillist, Message


@app.task
def start_maillist(maillist_id):
    """
    Запуск рассылки
    """
    maillist = Maillist.objects.get(id=maillist_id)
    op_code = maillist.operator_code
    tag = maillist.tag
    customers = Customer.objects.filter(
        Q(operator_code__exact=op_code) & Q(tag__exact=tag)
    )
    for customer in customers:
        message = Message(
            status="Pending",
            maillist=maillist,
            customer=customer
        )
        message.save()
        msg_id = message.id
        phone = message.customer.phone_number
        text = maillist.text
        send_message.delay(msg_id, phone, text)

@app.task
def send_message(msg_id, phone, text):
    """
    Отправка сообщения
    """
    url = "{}/send/{}".format(PROBE_SERVER_URL, msg_id)
    data = {
        "id": msg_id,
        "phone": phone,
        "text": text
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(TOKEN),
        "Content-Type": "application/json"
    }
    
    counter = 0
    while counter < 3:
        response = requests.post(
            url=url,
            data=json.dumps(data),
            headers=headers
        )
        if response.status_code == 200:
            message = Message.objects.get(id=msg_id)
            message.status = "Success"
            message.save()
            return True
        else:
            counter += 1
            time.sleep(300)
    message = Message.objects.get(id=msg_id)
    message.status = "Failed"
    message.save()
    return True
