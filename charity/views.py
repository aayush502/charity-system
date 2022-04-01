from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from user.models import NewUser
from .models import *
import pdb
import stripe
from django.contrib.auth.models import User
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from .forms import *
from charity.tasks import *
import os, sys, subprocess, platform
import pdfkit
from .process import html_to_pdf 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from django.views.decorators.csrf import csrf_exempt
import json
stripe.api_key = "sk_test_51JtRchSEz4lBqp0qwWE1jwZzVB39QlTrZFfiNTx0duNpox7TMO2SkpkjWVncXJz3BRSHxx7DFxdpxdX2Lai7t8RA00RKYenJJk"

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
        reason = request.POST['reasons']
        amount = request.POST['amount']
        organization = request.POST['org']
        document = request.FILES['doc']
        images = request.FILES.getlist('images')
        if(len(images)== 2):
            fund_request=FundRequestModel.objects.create(name=name, address=address, phone=phone, email=email, description=description, reason=reason, amount=amount, organization_name=organization, document=document, current_user = request.user.id)
            MultipleImage.objects.create(image1 = images[0],image2 = images[1], fund=fund_request)
            messages.success(request, "Your request has been submitted and will be verified by admins.")
            return redirect('/')
        else:
            messages.error(request, "upload 2 images")
            return redirect('fund_request')    

def bubble_sort(arr):
    number=len(arr)
    for i in range(number-1):
        for j in range(0, number-i-1):
            if arr[j] < arr[j+1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    final_fund = list(dict.fromkeys(arr))
    return final_fund

class Requests(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            user = NewUser.objects.all()
            fund_request = FundRequestModel.objects.all()
            data = []
            for u in user:
                for f in fund_request:
                    if(u.id == int(f.current_user) and u.is_ngo==False and f.verification_status==True):
                        data.append(f)
            arr=[]
            for f in data:
                arr.append(f.amount)
            fund_array = bubble_sort(arr)
            fund_data=[]
            for a in fund_array:
                for f in data:
                    if a==f.amount:
                        fund_data.append(f)
            images = MultipleImage.objects.all()  
            return render(request, "charity/home.html", context={"data":fund_data, "img":images})

class NgoRequestView(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            user = NewUser.objects.all()
            fund_request = FundRequestModel.objects.all()
            data = []
            for u in user:
                for f in fund_request:
                    if(u.id == int(f.current_user) and u.is_ngo==True and f.verification_status==True):
                        data.append(f)
            arr=[]
            for f in data:
                arr.append(f.amount)
            fund_array= bubble_sort(arr)
            fund_data=[]
            for a in fund_array:
                for f in data:
                    if int(a)==f.amount:
                        fund_data.append(f)
            images = MultipleImage.objects.all()
            return render(request, "charity/ngo_request.html", context={"data":fund_data, "img": images})

class PendingRequest(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            user = NewUser.objects.all()
            fund_request = FundRequestModel.objects.all()
            data = []
            for u in user:
                for f in fund_request:
                    if(u.id == int(f.current_user) and f.verification_status==None):
                        data.append(f)
            arr=[]
            for f in data:
                arr.append(f.amount)
            fund_array= bubble_sort(arr)
            fund_data=[]
            for a in fund_array:
                for f in data:
                    if int(a)==f.amount:
                        fund_data.append(f)
            images = MultipleImage.objects.all()
            return render(request, "charity/pending-requests.html", context={"data":fund_data, "img":images})

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
        fund_model = FundRequestModel.objects.filter(id=id)
        for f in fund_model:
            amount = request.POST['amount']
            recieved_amount = int(f.amount_recieved)
            recieved_amount += int(amount)
            fund_model.update(amount_recieved = recieved_amount)
        request_list = FundRequestModel.objects.all()
        fund_list = []
        for requests in request_list:
            if(donor.donated_to == requests.id):
                fund_list.append(requests)
        context={ 
            "donor":donor, 
            "reciever":fund_list[0]
            }
        return redirect('payment_success', id=donor.id)

class Success(View):
    def get(self, request, id):
        donor =DonorList.objects.filter(id=id).first()
        fund_model = FundRequestModel.objects.all()
        fund_list = []
        for requests in fund_model:
            if(donor.donated_to == requests.id):
                fund_list.append(requests)
        context={ 
            "donor":donor, 
            "reciever":fund_list[0]
        }
        return render(request, "charity/success.html", context)

class GeneratePdf(View):
    def get(self, request,id):
        # config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        # if platform.system() == "Windows":
        #     pdfkit_config = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
        # else:
        #     os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable) 
        #     WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], 
        #         stdout=subprocess.PIPE).communicate()[0].strip()
        #     pdfkit_config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)
        if 'DYNO' in os.environ:
                print ('loading wkhtmltopdf path on heroku')
                WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf-pack')],stdout=subprocess.PIPE).communicate()[0].strip()
        else:
            print ('loading wkhtmltopdf path on localhost')
            WKHTMLTOPDF_CMD =  pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        pdf = pdfkit.from_url(f'127.0.0.1:8000/payment_success/{id}',False,configuration=WKHTMLTOPDF_CMD)
        # pdf = pdfkit.from_url(f'127.0.0.1:8000/payment_success/{id}',False)
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="donate.pdf"'
        return response

class SuccessPayment(View):
    def get(self, request):
        return render(request, "charity/success.html", context={})

@csrf_exempt
def verify_payment(request, id):
    data = request.POST
    product_id = data['product_identity']
    token = data['token']
    amount = data['amount']
    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
        "token": token,
        "amount": amount
    }
    headers = {
        "Authorization": "Key test_secret_key_91de2c5b38144ba59b14fe0458a84276"
    }
    response = requests.post(url, payload, headers = headers)
    response_data = json.loads(response.text)
    status_code = str(response.status_code)
    donor = DonorList.objects.create(email = request.user.email, name = response_data['user']['name'], amount=int(amount), message='donation', donated_to=id, current_user=request.user.id)
    if status_code == '400':
        response = JsonResponse({'status':'false', 'message': response_data['detail']}, status=500)
        return response
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_data)
    return JsonResponse("Thanks for your donation", safe=False)   

class AdminRequestView(View):
    def get(self, request):
        if 'user_id' not in request.session:
            return redirect('/login')
        else:
            data = FundRequestModel.objects.all()
            image = MultipleImage.objects.all()
            return render(request, "charity/admin-verify-request.html", context={"data":data,"img":image})

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
    user = NewUser.objects.filter(id=id)
    user.verification_true()
    return redirect('admin-verify-ngo')

def ngo_verification_false(self, id):
    ngo_email_false_task.delay(id)
    return redirect('admin-verify-ngo')

class RequestsView(View):
    def get(self, request, pk):
        fund = FundRequestModel.objects.filter(id=pk).first()
        image = MultipleImage.objects.filter(fund=pk).first()
        donor_list = DonorList.objects.all()
        lists = []
        for donor in donor_list:
            if(donor.donated_to == fund.id):
                lists.append(donor)
        return render(request, "charity/request_view.html", context={"data":fund, "donor":lists, "img":image})

class Search(View):
    def post(self, request):
        searched = request.POST['search']
        found = FundRequestModel.objects.filter(reason__icontains=searched)
        fund_request_data = FundRequestModel.objects.all()
        image = MultipleImage.objects.all()
        return render(request, "charity/search.html", context={"data":fund_request_data,"found":found, "img":image})

class UpdateRequest(View):
    def get(self, request , id):
        fund_request = FundRequestModel.objects.filter(id=id).first()
        images = MultipleImage.objects.filter(fund=id).first()
        return render(request, "charity/update_request.html", context={"data":fund_request, "img":images})
    
    def post(self, request, id):
        fund_request = FundRequestModel.objects.get(id=id)
        fund_images = MultipleImage.objects.filter(fund=fund_request)
        if request.FILES.get('doc'):
            if len(request.FILES.get('doc'))!=0:
                if len(fund_request.document) > 0:
                    os.remove(fund_request.document.path)
                fund_request.document = request.FILES.get('doc')
        if len(request.FILES.getlist('images')) != 0:
            if len(fund_images[0].image1 and fund_images[0].image2) > 0:
                os.remove(fund_images[0].image1.path)
                os.remove(fund_images[0].image2.path)
            get_images = request.FILES.getlist('images')
            img = fund_images[0]
            img.image1=get_images[0]
            img.image2=get_images[1]
            img.save()
        fund_request.name = request.POST['name']
        fund_request.address = request.POST['address']
        fund_request.phone = request.POST['phone']
        fund_request.email = request.POST['email']
        fund_request.description = request.POST['desc']
        fund_request.organization = request.POST['org']
        fund_request.save()
        messages.success(request, "Updated Succesfully")
        return redirect(f'requests',pk=fund_request.id)

def delete(request, id):
    if request.method == "GET":
        fund_request = FundRequestModel.objects.get(id=id)
        return render(request, "charity/delete.html", context={"data":fund_request})
    if request.method == "POST":
        fund_request = FundRequestModel.objects.get(id=id)
        images = MultipleImage.objects.filter(fund=fund_request)
        fund_request.delete()
        for img in images:
            img.delete()
        return redirect('/')

class Testimonials(View):
    def get(self, request):
        donor = DonorList.objects.filter(email=request.user.email)
        data = Testimonial.objects.filter(verification_status=True)
        page = request.GET.get('page', 1)
        paginator = Paginator(data, 3)
        try:
            data_list = paginator.page(page)
        except PageNotAnInteger:
            data_list = paginator.page(1)
        except EmptyPage:
            data_list = paginator.page(paginator.num_pages)
        return render(request, "charity/testimonials.html", context={"data":data_list, "donor":donor})

class PostTestimonial(View):
    def get(self, request):
        data = Testimonial.objects.all()
        return render(request, "charity/testimonial-form.html", context={})
    
    def post(self, request):
        name = request.POST['name']
        profession = request.POST['profession']
        review_message = request.POST['desc']
        donated_to = request.POST['reasons']
        image = request.FILES['image']
        Testimonial.objects.create(name=name, profession=profession,review_message=review_message, donated_to=donated_to, image=image)
        return redirect('testimonials')

class AdminVerifyTestimonials(View):
    def get(self, request):
        data = Testimonial.objects.all()
        return render(request, "charity/admin-verify-testimonials.html", context={"data":data})

def testimonial_verified_as_true(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.verification_true()
    return redirect('admin-verify-testimonial')

def testimonial_verified_as_false(request, id):
    testimonial = get_object_or_404(Testimonial, id=id)
    testimonial.verification_false()
    return redirect('admin-verify-testimonial')