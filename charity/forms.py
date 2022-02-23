from django import forms
from .models import *
  
class FundRequestForm(forms.ModelForm):
  
    class Meta:
        model = FundRequestModel
        fields = ['description', 'amount', 'image', 'document']