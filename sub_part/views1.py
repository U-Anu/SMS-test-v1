from django.http import HttpResponse, HttpResponseRedirect
import json, random, string
from django.shortcuts import render, redirect, get_object_or_404
# from pesanile_accounting.normal_views import account_creation_finance
from pesanile_accounting.scripts_pr import receivable_atomic
from pesanile_accounting.views_ms import post_receivable_and_payable_transaction_ms
from sub_part.models import *
from sub_part.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .password import generate_password
from .emails import new_staff_account_email
from django.db.models import Count, Sum
from .emails import new_staff_account_email, send_email_notification,send_email_notification1
from datetime import datetime, timedelta, date, time
from django.template.defaultfilters import floatformat
import pandas as pd
from payment.models import PaymentKeys
from .sms import *
from .decorators import *
import calendar
from django.utils import timezone
from num2words import num2words  
from .accounts import *
from .api_call import *
import json
from decimal import Decimal
import requests
import re
from concurrent.futures import ThreadPoolExecutor
from sub_part.models import Currency as sub_part_Currency
from django.contrib.auth.hashers import make_password
from reports.models import *
BASE_URL = 'https://bbaccountingsms.pythonanywhere.com/'
# PACKAGE_URL = 'https://roisoukv1.pythonanywhere.com/'
PACKAGE_URL='http://127.0.0.1:8501/'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from urllib.parse import urlparse

from .models import *
from .serializers import *
from celery import shared_task
User = get_user_model()

@login_required
def feedback_list(request):
    # POST → SAVE ONLY FEEDBACK REASON
    if request.method == "POST":
        reason_text = request.POST.get("reason")

        if reason_text:
            Feedback_Reasons.objects.create(
                reason=reason_text
            )

        return redirect("feedback_list")

    # GET → LIST ONLY FEEDBACK
    feedbacks = Feedback.objects.select_related("user", "reason").order_by("-created_at")

    return render(
        request,
        "feedback_list.html",
        {
            "feedbacks": feedbacks,
        }
    )

@login_required
def feedback_create(request):
    print('hhshshhshs',request.META.get('HTTP_REFERER', '/'))

    referer = request.META.get('HTTP_REFERER', '/')
    path = urlparse(referer).path      # '/collect_fees'
    last_name = path.strip('/').split('/')[-1]
    name = path.strip('/').split('/')[-1].replace('_', ' ').title()
    print(name,'nameeeeeeeeeeeeee')
    if re.search(r'/\d+/?$', path) and request.method == "GET":
        return redirect(path)
    if request.method == "POST":
        reason_id = request.POST.get("reason")
        feedback_text = request.POST.get("feedback")
        return_url = request.POST.get("last_name")
        print('reason_id',reason_id)
        print('yyyyyyyyyyy',request.POST)
        reason = get_object_or_404(Feedback_Reasons, id=reason_id)
        Feedback.objects.create(
            user=request.user,
            reason=reason,
            feedback=feedback_text,
            name=last_name,
            endpoint=referer
        )
        print('the request user type is ',request.user.user_type)
        if request.user.user_type == 'Student':
            print('in student redirect')
            return redirect(f"student/{return_url}")
        elif request.user.user_type == 'parent':
            print('in parent redirect')
            return redirect(f"parent/{return_url}")
        else:
            return redirect(return_url)

    reasons = Feedback_Reasons.objects.all()


    return render(
        request,
        "feedback_create.html",
        {
            "reasons": reasons,
            "last_name": last_name,
            "name": name,
        }
    )