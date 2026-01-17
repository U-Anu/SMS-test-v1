from django.db import models
from sub_part.models import *

# Create your models here.


class PaymentKeys(models.Model):
    razorpay_key_id=models.CharField(max_length=500,blank=True,null=True)
    razorpay_key_secret=models.CharField(max_length=500,blank=True,null=True)
    mpesa_passkey=models.CharField(max_length=500,blank=True,null=True)
    mpesa_consumer_key=models.CharField(max_length=500,blank=True,null=True)
    mpesa_consumer_secret=models.CharField(max_length=500, blank=True, null=True)
    seleted_payment=models.CharField(max_length=500, blank=True, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)

    
    