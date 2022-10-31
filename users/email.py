from django.conf import settings
from django.core.mail import send_mail


def email_service(subject, msg, recipient_email):
    recipient_list = [recipient_email]
    send_mail(from_email=settings.DEFAULT_FROM_EMAIL, subject=subject, message=msg, recipient_list=recipient_list)
