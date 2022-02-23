from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from user.models import NewUser
from .models import *
import pdb
import stripe
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from .forms import *
stripe.api_key = "sk_test_51JtRchSEz4lBqp0qwWE1jwZzVB39QlTrZFfiNTx0duNpox7TMO2SkpkjWVncXJz3BRSHxx7DFxdpxdX2Lai7t8RA00RKYenJJk"
class HomeView(View):
    def get(self, request):
        # if 'user_id' not in request.session:
        #     return redirect('/login')
        # else:
        return render(request, "charity/home.html", context={})
class AboutView(View):
    def get(self, request):
        return render(request, "charity/about.html", context={})

class RequestFund(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            data = FundRequestModel.objects.all()
            return render(request, "charity/request_fund.html", context={"data": data})


    def post(self, request):
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']
        email = request.POST['email']
        description = request.POST['desc']
        amount = request.POST['amount']
        image = request.FILES['image']
        document = request.FILES['doc']
        FundRequestModel.objects.create(name=name, address=address, phone=phone, email=email, description=description, amount=amount, image=image, document=document, current_user = request.user.id)
        messages.success(request, "Your request has been submitted and will be verified by admins.")
        return redirect('requests')

class Requests(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            # ngo_data = NGO.objects.all()
            fund_request_data = FundRequestModel.objects.all()
            # a = []
            # for data in ngo_data:
            #     for fund_data in fund_request_data:
            #         if(data.current_user != fund_data.current_user):
            #             a.append(fund_data)

            return render(request, "charity/requests.html", context={"data":fund_request_data})
    
def charge(request, id):
    user = FundRequestModel.objects.get(id=id)
    if request.method == "GET":
        return render(request, "charity/payment.html", context={"user":user})

    else:
        print("Data: ", request.POST)
        customer = stripe.Customer.create(
            email = request.POST['email'],
            name=request.POST['name'],
            source = request.POST['stripeToken']
        )
        charge = stripe.Charge.create(
            customer=customer,
            amount = int(request.POST['amount'])*100,
            currency="INR",
            description = "Donation",
        )
    return redirect('success')

def success(request):
    return render(request, "charity/success.html", context={})

class khaltiView(View):
    def get(self, request):
        return render(request, "charity/khalti.html", context={})

    def post(self, request):
        import requests
        url = "https://khalti.com/api/v2/merchant-transaction/"
        payload = {}
        headers = {
        "Authorization": "Key test_secret_key_f59e8b7d18b4499ca40f68195a846e9b"
        }
        response = requests.get(url, payload, headers = headers)

class AdminRequestView(View):
    def get(self, request):
        data = FundRequestModel.objects.all()
        return render(request, "charity/admin-verify-request.html", context={"data":data})

def verification_true(self,id):
    fund_request = get_object_or_404(FundRequestModel, id=id)
    fund_request.verification_true()
    subject = 'Request Verified'
    message = f'Hi {fund_request.name}, your request for the charity is verified by admins. you will now recieve funds.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [fund_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('admin-verify-request')

def verification_false(self, id):
    fund_request = get_object_or_404(FundRequestModel, id=id)
    fund_request.verification_false()
    subject = 'Request Rejected'
    message = f'Hi {fund_request.name}, your request for the charity in charity system is rejected by admins. Request again with proper documents'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [fund_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('admin-verify-request')

class NGOView(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            return render(request, "charity/ngo-form.html", context={})
    
    def post(self, request):
        ngo_name = request.POST['name']
        ngo_head = request.POST['head']
        phone = request.POST['phone']
        email = request.POST['email']
        certificate1 = request.FILES['certificate1']
        certificate2 = request.FILES['certificate2']
        profile = request.FILES['profile']
        NGO.objects.create(ngo_name=ngo_name, head_of_ngo=ngo_head, contactNo=phone,email=email, registration_cerificate_Trust_Society=certificate1, certificate_12A=certificate2, beneficiary_profiles=profile, current_user = request.user.id)
        messages.success(request, "Your request has been submitted and will be verified by admins.")
        return redirect("home")


class NGOVerification(View):
    def get(self, request):
        ngo = NGO.objects.all()
        return render(request, "charity/admin-verify-ngo.html", context={"ngo":ngo})

def ngo_verification_true(self,id):
    # is_ngo = NewUser.objects.get(id=request.user.id)
    # is_ngo.verification_true()
    ngo_request = get_object_or_404(NGO, id=id)
    ngo_request.verification_true()
    subject = 'NGO Verified'
    message = f'Hi {ngo_request.ngo_name}, your request for the ngo creation is successful. '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ngo_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('admin-verify-ngo')

def ngo_verification_false(self, id):
    ngo_request = get_object_or_404(NGO, id=id)
    ngo_request.verification_false()
    subject = 'Request Rejected'
    message = f'Hi {ngo_request.name}, your request for the ngo creation is denied by admins please send proper details to register you ngo'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [ngo_request.email]
    send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('admin-verify-ngo')

class RequestsView(View):
    def get(self, request, id):
        fund = FundRequestModel.objects.filter(id=id).first()
        return render(request, "charity/request_view.html", context={"data":fund})

class NgoRequestView(View):
    def get(self, request):
        ngo_data = NGO.objects.all()
        fund_request_data = FundRequestModel.objects.all()
        a = []
        for data in ngo_data:
            for fund_data in fund_request_data:
                if(data.current_user == fund_data.current_user):
                    a.append(fund_data)        
        return render(request, "charity/ngo_request.html", context={"data":a})