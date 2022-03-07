from email import message
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
from charity.tasks import *
import pdfkit
# from .pdfconverter import html_to_pdf
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
        images = request.FILES.getlist('images')
        document = request.FILES['doc']
        for image in images:
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
        donor = DonorList.objects.create(email=request.POST['email'], name=request.POST['name'], amount=request.POST['amount'], message=request.POST['desc'], current_user = request.user.id, donated_to = id)
        request_list = FundRequestModel.objects.all()
        fund_list = []
        for requests in request_list:
            if(donor.donated_to == requests.id):
                fund_list.append(requests)
        # pdf = pdfkit.from_url(f'127.0.0.1:8000/charge/{id}', "donate.pdf")  
        return render(request, "charity/success.html", context={"donor":donor, "reciever":fund_list[0]})

# class GeneratePdf(View):
#     def get(self, request, id):
#         config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
#         pdf = pdfkit.from_url(f'127.0.0.1:8000/charge/{id}',False,configuration=config)
#         response = HttpResponse(pdf,content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="donate.pdf"'
#         return response

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
    send_mail_true_task.delay(id)
    return redirect('admin-verify-request')

def verification_false(self, id):
    send_mail_false_task.delay(id)
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
    ngo_email_true_task.delay(id)
    return redirect('admin-verify-ngo')

def ngo_verification_false(self, id):
    ngo_email_false_task.delay(id)
    return redirect('admin-verify-ngo')

class RequestsView(View):
    def get(self, request, id):
        fund = FundRequestModel.objects.filter(id=id).first()
        donor_list = DonorList.objects.all()
        # fund_request = FundRequestModel.objects.all()
        lists = []
        for donor in donor_list:
            if(donor.donated_to  == fund.id):
                lists.append(donor)
        return render(request, "charity/request_view.html", context={"data":fund, "donor":lists})

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