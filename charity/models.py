from distutils.command.upload import upload
from statistics import mode
from django.db import models
from django_currentuser.middleware import get_current_authenticated_user, get_current_user
import datetime
class FundRequestModel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True)
    description = models.CharField(max_length=1000, null=False)
    reason = models.CharField(max_length=50, null=True)
    amount = models.IntegerField(null=False, default=False)
    amount_recieved = models.BigIntegerField(null=True, default=0)
    organization_name = models.CharField(max_length=100, blank=True, null=True)
    document = models.FileField(upload_to= 'documents/')
    verification_status = models.BooleanField(null=True)
    postted_at = models.DateField(default=datetime.date.today, null=True)
    current_user = models.CharField(default=get_current_user, blank=True, max_length=40)
    def __str__(self):
        return f"{self.reason} at {self.postted_at}"

    def verification_true(self):
        self.verification_status = True
        self.save()

    def verification_false(self):
        self.verification_status = False
        self.save()
    
    # def get_image_filename(instance, filename):
    #     id=instance.fund.id
    #     return "fund_images/%s"%(id)

class MultipleImage(models.Model):
    fund = models.ForeignKey(FundRequestModel, on_delete=models.CASCADE)
    image1 = models.ImageField(upload_to='images/', null=True)
    image2 = models.ImageField(upload_to='images/', null=True)

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