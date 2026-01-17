import time
from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

class MiddlewareExecutionStart(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request): 
        print('request.user in middleware',request.user)
        branch_id=None
        if request.user.is_authenticated and not request.user.is_superuser:
            # print('request.user in middleware if',request.user)
            if request.user.school:
                branch_id=Branch.objects.filter(school__school_id=request.user.school.school_id).first()
                # print('the branch i is ',branch_id)
                general_setting=GeneralSetting.objects.filter(branch=branch_id).last()
                # print('general_setting in middleware',general_setting)
            else:
                branch_id=None
                general_setting=GeneralSetting.objects.all().last()
        else:
            branch_id=None
            general_setting=GeneralSetting.objects.all().last()
        # print('branch_id in middlewaddddddre',branch_id)
        
        if general_setting:
            request.Session = general_setting.session
        else:
            request.Session = None
        if request.user.is_authenticated and not request.user.is_superuser  and not request.user.is_school_admin :
            if request.user.user_type=='Student':
                request.student=StudentAdmission.objects.filter(user_student=request.user,session=request.Session ,branch=branch_id).last()
                if request.student:
                    request.student=StudentAdmission.objects.filter(user_student=request.user).last()
            elif request.user.user_type=='Parent':
                request.parent=StudentAdmission.objects.filter(user_parent=request.user,session=request.Session,branch=branch_id).last()
            else:
                print('request.user_middelware',request.user)
                access=AddStaff.objects.filter(user=request.user).last()
                print('the acess in middleware is ',access)
                print('the acess in middleware is ',access.roles)
                print('the acess in middleware is ',type(access.roles.permissions))
                if access:                    
                    request.permissions=access.roles.permissions 
                    if not access.roles.permissions:
                        request.permissions=[]
                        logout(request)
                        return redirect("signin")         
                else:
                    logout(request)
                    return redirect("signin")        
        else:
            request.permissions=[]

        records=Modules.objects.all().first()
        if records and records.system:
            request.system_modules=records.system
        else:
            request.system_modules=[]
        if records and records.student:
            request.student_modules=records.student
        else:
            request.student_modules=[]
        if records and records.parent:
            request.parent_modules=records.parent
        else:
            request.parent_modules=[]
        response = self.get_response(request)
        return response

# def process_exception(self,request,exception):
#     return HttpResponse('<h3>Currently We Are Facing Technical Isses</h3>')

# def process_exception(self,request,exception):        
#     return render(request,'error.html',{'error':exception})