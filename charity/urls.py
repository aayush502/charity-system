from unicodedata import name
from django.http import request
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import re_path, url
urlpatterns = [
    path('',Requests.as_view(), name='home'),
    path('about', AboutView.as_view(), name="about"),
    url(r'^fund_request/$', RequestFund.as_view(), name="fund_request"),
    path('pending-requests', PendingRequest.as_view(), name="pending-requests"),
    path('charge/<int:id>', charge, name='charge'),
    path('ngo', NGOView.as_view(), name="ngo"), 
    path('ngo-request', NgoRequestView.as_view(), name="ngo-request"),
    path("success", SuccessPayment.as_view(), name="success"),
    url(r'payment_success/(?P<id>\d+)/$', Success.as_view(), name="payment_success"),
    url(r'pdf/(?P<id>\d+)/$', GeneratePdf.as_view(), name="pdf"),
    path("admin-verify-request", AdminRequestView.as_view(), name="admin-verify-request"),
    path("admin-verify-ngo", NGOVerification.as_view(), name="admin-verify-ngo"),
    path("request_verified_as_true/<id>", verification_true, name="request_verified_as_true"),
    path("request_verified_as_false/<id>", verification_false, name="request_verified_as_false"),
    path("ngo_verified_as_true/<id>", ngo_verification_true, name="ngo_verified_as_true"),
    path("ngo_verified_as_true/<id>", ngo_verification_false, name="ngo_verified_as_false"),
    url(r'^requests/(?P<pk>[\w-]+)/$', RequestsView.as_view(), name="requests"),
    path('search',Search.as_view(), name="search"),
    path('update/<id>', UpdateRequest.as_view(), name="update"),
    path('delete/<id>', delete, name="delete"),
    path('testimonials', Testimonials.as_view(), name="testimonials"),
    path('create-testimonials', PostTestimonial.as_view(), name="create-testimonials"),
    path("admin-verify-testimonial", AdminVerifyTestimonials.as_view(), name="admin-verify-testimonial"),
    path("testimonial_verified_as_true/<id>", testimonial_verified_as_true, name="testimonial_verified_as_true"),
    path("testimonial_verified_as_false/<id>", testimonial_verified_as_false, name="testimonial_verified_as_false"),
    path('verify-khalti-payment/<int:id>', verify_payment, name="verify-khalti-payment"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
