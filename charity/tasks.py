import imp
from celery import shared_task
from time import sleep
from django.core.mail import send_mail
from charity.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

@shared_task
def sleepy(duration):
    sleep(duration)
    return None

@shared_task 
def send_mail_true_task(id):
    sleep(5)
    fund_request = get_object_or_404(FundRequestModel, id=id)
    fund_request.verification_true()
    subject = 'Request Verified'
    message = f'Hi {fund_request.name}, your request for the charity is verified by admins. you will now recieve funds.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [fund_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return None

@shared_task 
def send_mail_false_task(id):
    sleep(5)
    fund_request = get_object_or_404(FundRequestModel, id=id)
    fund_request.verification_false()
    subject = 'Request Rejected'
    message = f'Hi {fund_request.name}, your request for the charity in charity system is rejected by admins. Request again with proper documents'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [fund_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return None
    
@shared_task    
def ngo_email_true_task(id):
    sleep(5)
    ngo_request = get_object_or_404(NGO, id=id)
    ngo_request.verification_true()
    subject = 'NGO Verified'
    message = f'Hi {ngo_request.ngo_name}, your request for the ngo creation is successful. '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ngo_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return None

@shared_task    
def ngo_email_false_task(id):
    sleep(5)
    ngo_request = get_object_or_404(NGO, id=id)
    ngo_request.verification_false()
    subject = 'Request Rejected'
    message = f'Hi {ngo_request.name}, your request for the ngo creation is denied by admins please send proper details to register you ngo'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ngo_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return None