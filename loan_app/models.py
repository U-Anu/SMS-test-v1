from django.db import models

# Create your models here.

class LoanRegistration(models.Model):
    loan_id = models.CharField(max_length=100, primary_key=True)
    loan_no = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=500, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.loan_id)