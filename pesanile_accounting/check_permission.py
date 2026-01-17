from sub_part.models import User
from django.apps import apps
pre_models = ['Currency','AccountTypeCategory','AccountType','AccountCategory','AssetTypeCategory','AssetType','GLLine']
def get_model_instance(app_name, model_name):
    print(app_name, model_name)
    try:
        model = apps.get_model(app_name, model_name=model_name)
        return model
    except Exception as error:
        print('error ',error)

def check_user_role_return_db(app_name, model_name, request, list_all=False):
    try:
        model = get_model_instance(app_name,model_name)
        print('model ',model)
        print('list_all ',list_all)
        if model is None:
            return []
        if request.user.is_superuser or request.user.is_school_admin:
            obj = model.objects.all()
        if request.user.is_school_admin:
            obj = model.objects.all()

        # if request.user.is_customer:
        #     if list_all:
        #         obj = model.objects.all()
        #     else:
        #         obj = model.objects.filter(company_name=request.user.company_name)
        # if not request.user.is_customer and not request.user.is_superuser or request.user.is_school_admin:
        #     if model_name in pre_models:
        #         obj = model.objects.all()
        #     else:
        #         obj = model.objects.filter(company_name=request.user.company_name)
        if list_all:
            obj = model.objects.all()
        print('obj ', obj)
        return obj
    except Exception as error:
        print('error ',error)
        return model.objects.none()

def has_add_access(request):
    if request.user.is_superuser or request.user.is_school_admin:
        obj = 'yes'
    if request.user.is_customer:
        if list_all:
            obj = model.objects.all()
        else:
            obj = model.objects.filter(company_name=request.user.company_name)
    if not request.user.is_customer and not request.user.is_superuser or request.user.is_school_admin:
        obj = model.objects.filter(branch_name=request.user.branch_name)
    if list_all:
        obj = model.objects.all()