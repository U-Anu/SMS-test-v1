from django.contrib.auth.models import User
from .models import *

def users_and_projects(request):
    branch_id=None
    if request.user.is_authenticated and not request.user.is_superuser:
        branch_id=Branch.objects.filter(school__school_id=request.user.school.school_id).first()
        general_setting=GeneralSetting.objects.filter(branch=branch_id).last()
    else:
        branch_id=None
        general_setting=GeneralSetting.objects.all().last()
    print('branch_id in middlewaddddddre',branch_id)
    if not general_setting:
        general_setting=[]

    return {'general_setting': general_setting}

def alert_messages(request):
    message = None

    if request.user.is_authenticated:
        print('request.user in context processor', request.user)
        message = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).last()
        print('messages in context processor', type(message))

    return {'alert_messages': message}
