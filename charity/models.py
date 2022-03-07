from django.conf import settings
from django.db import models
from django_currentuser.middleware import get_current_authenticated_user, get_current_user
import django.http.request as request
class FundRequestModel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True)
    description = models.CharField(max_length=1000, null=False)
    amount = models.IntegerField(null=False, default=False)
    image = models.ImageField(upload_to= 'images/') 
    document = models.FileField(upload_to= 'documents/')
    verification_status = models.BooleanField(null=True)
    current_user = models.CharField(default=get_current_user, blank=True, max_length=40)
    def __str__(self):
        return self.name

    def verification_true(self):
        self.verification_status = True
        self.save()

    def verification_false(self):
        self.verification_status = False
        self.save()

class NGO(models.Model):
    ngo_name = models.CharField(max_length=30,blank=True)
    head_of_ngo = models.CharField(max_length=30,blank=True)
    contactNo = models.CharField(max_length=10,blank=True)
    email = models.EmailField(blank=True)
    registration_cerificate_Trust_Society = models.FileField(upload_to='verification',blank=True)
    certificate_12A = models.FileField(upload_to='verification',blank=True)
    beneficiary_profiles = models.FileField(upload_to='verification',blank=True)
    verification_status = models.BooleanField(default=None,blank=True,null=True)
    current_user = models.CharField(default=get_current_user, blank=True, max_length=40)
    def verification_true(self):
        self.verification_status=True        
        self.save()

    def verification_false(self):
        self.verification_status = False
        self.save()

    def get_user(self,user):
        self.ngo_user = user
        self.save()

    def __str__(self):
        return self.ngo_name


class DonorList(models.Model):
    email = models.EmailField(blank=True)
    name = models.CharField(max_length=100, blank=True)
    amount = models.BigIntegerField(blank=True)
    message = models.CharField(max_length=1000, blank=True)
    donated_to = models.IntegerField(blank=True)
    current_user = models.BigIntegerField(blank=True)