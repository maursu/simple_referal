import time

from celery import shared_task
from django.contrib.auth import get_user_model

from config.celery import app


@app.task
def send_login_code():
    time.sleep(1)


@app.task
def delete_login_code(phone_number):
    User = get_user_model()
    user = User.objects.get(phone_number=phone_number)
    user.login_code = hash("1243")
    user.save()
