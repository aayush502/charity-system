from unicodedata import name
from django.http import request
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import re_path, url
urlpatterns = [
    path('',HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name="about"),
    url(r'^fund_request/$', RequestFund.as_view(), name="fund_request"),
    path('requests', Requests.as_view(), name="requests"),
    path('charge/<int:id>', charge, name="charge"),
    path('ngo', NGOView.as_view(), name="ngo"), 
    path('ngo-request', NgoRequestView.as_view(), name="ngo-request"),
    # path('pdf/<int:id>', GeneratePdf.as_view(), name="pdf"),
    path('khalti', khaltiView.as_view(), name="khati"),
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
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
