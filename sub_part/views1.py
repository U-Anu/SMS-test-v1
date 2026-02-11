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
            return redirect(f"student/{'feedback_list'}")
        elif request.user.user_type == 'parent':
            print('in parent redirect')
            return redirect(f"parent/{'feedback_list'}")
        else:
            return redirect('feedback_list')

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
    
    
    
    

# def online_exam_assign(request, pk):
#     # try:
#         branch_name = request.session.get('branch_id', None)
#         if branch_name:
#             branch_id = branch_name
#         else:
#             branch_id = None
#             print("branch_name@@@", branch_name)

#         student_answer = AnswerPeperSubmit.objects.filter(student_answers=pk)
#         print("student_answer+++", student_answer)

#         # 👉 GET FIRST OBJECT FOR REUSE
#         first_obj = student_answer.first()
#         question_paper = first_obj.questiones.question_paper
#         student_obj = first_obj.student_answers.student

#         # ✅ CHECK EXISTING CORRECTION
#         existing_correction = PaperCorrection.objects.filter(
#             student_id=student_obj.id,
#             question_paper=question_paper
#         ).order_by('-id').first()

#         final_mark = request.POST.get('final_mark')
#         pass_mark = request.POST.get('pass_mark')
#         paragraph_value = request.POST.get('paragraph_value')

#         paragraph_mark = int(paragraph_value) if paragraph_value else 0
#         final_marks = int(final_mark) if final_mark else 0
#         total_marks = paragraph_mark + final_marks

#         if request.method == "POST":
#             for question_id in student_answer:
#                 selected_option = request.POST.get(f"option_{question_id.questiones.id}")
#                 print("selected_option", selected_option)
#                 question_id.options = selected_option
#                 question_id.mark = question_id.questiones.mark
#                 question_id.validation = True
#                 question_id.branch_id = branch_id
#                 question_id.save()

#             # ✅ UPDATE INSTEAD OF ALWAYS CREATE
#             # ✅ UPDATE LAST RECORD IF EXISTS, ELSE CREATE NEW
#             last_correction = PaperCorrection.objects.filter(
#                 student_id=student_obj.id,
#                 question_paper=question_paper
#             ).order_by('-id').first()

#             if last_correction:
#                 last_correction.total_mark = total_marks
#                 last_correction.is_pass = total_marks >= int(pass_mark)
#                 last_correction.branch_id = branch_id
#                 last_correction.save()
#             else:
#                 PaperCorrection.objects.create(
#                     student_id=student_obj.id,
#                     question_paper=question_paper,
#                     total_mark=total_marks,
#                     is_pass=total_marks >= int(pass_mark),
#                     branch_id=branch_id
#                 )

#             # ✅ Redirect back to correction list page
#             return redirect('answer_paper_correction')

#         # Existing code for question paper info
#         for data in student_answer:
#             record = data.questiones.question_paper
#         single_value = QuestionPaper.objects.filter(id=record.id).last()
#         print("single_value", single_value)
         
#         context = {
#             "questions": student_answer,
#             "single_value": single_value,
#             "existing_correction": existing_correction,  # 👈 SEND TO TEMPLATE
#             "question_models": "active"
#         }
#         return render(request, "OnlineExamination/online_exam_assign.html", context)

    # except Exception as error:
    #     return render(request, "error.html", {"error": error})
