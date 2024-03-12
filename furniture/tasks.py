from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
import random
from .models import *


def r():
    x = random.randint(100, 1000)
    return x


x = r()

@shared_task
def send_email_task(email):
    try:
        send_mail(subject="Kompaniya ziyo nur",
                  message=f"sizning buyurma nomeringiz {x}",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[email],
                  fail_silently=False
                  )

        print("XAbar yuborildi !")
        return "Xabar yuborildi"
    except:
        print("XAbar yuborildi !")
        return "Xabar yuborilmadi!"


@shared_task
def send_email_admin_task(user, phone_number, *args):
    try:
        send_mail(subject="Kompaniya ziyo nur",
                  message=f"mijozning ismi va familiyasi {user} \
                            \n mijozning tel: raqami  {phone_number},\
                           mijozning buyurtma raqami : {x} \
                            mahsulotning nomlari {args},\
                           \n iltimos admin panelga qaren ",
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=['djamolovramazon90@gmail.com'],
                  fail_silently=False
                  )

        print("XAbar yuborildi 1!")
        return "Xabar yuborildi1"
    except:
        print("XAbar yuborildi1 !")
        return "Xabar yuborilmadi1 !"
