from pesanile_accounting.models import AssetTypeCategory,AssetType,GLLine
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from pesanile_accounting.check_permission import check_user_role_return_db
def exclude_field(field_name):
    return field_name not in ['created_at', 'updated_at', 'created_by','updated_by','company_name','branch_name']



@login_required(login_url='/')
def report_type_create(request):
    if request.method == 'POST':
        form = ReportTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_type_list')
    else:
        form = ReportTypeForm()
        context = {
                'form': form,
                'create_url': reverse('report_type_add'),
                'list_url': reverse('report_type_list'),
                "message": ""
            }
        
        template_name = 'pesanile_accounting/create_everything.html'
    return render(request, template_name, context)


@login_required(login_url='/')
def clcation_type_create(request):
    if request.method == 'POST':
        form = calculationTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('report_type_list')
    else:
        form = calculationTypeForm()
        context = {
                'form': form,
                'create_url': reverse('report_type_add'),
                'list_url': reverse('report_type_list'),
                "message": ""
            }
        
        template_name = 'pesanile_accounting/create_everything.html'
    return render(request, template_name, context)



@login_required(login_url='/')
def reportmapping_create(request):
    if request.method == 'POST':
        form = ReportmappingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reportmapping_list')
    else:
        form = ReportmappingForm()
        context = {
                'form': form,
                'create_url': reverse('reportmapping_add'),
                'list_url': reverse('reportmapping_list'),
                "message": ""
            }
        
        template_name = 'pesanile_accounting/create_everything.html'
    return render(request, template_name, context)


# def report_type_update(request, pk):
#     report_type = get_object_or_404(ReportType, pk=pk)
#     if request.method == 'POST':
#         form = ReportTypeForm(request.POST, instance=report_type)
#         if form.is_valid():
#             form.save()
#             return redirect('report_type_list')
#     else:
#         form = ReportTypeForm(instance=report_type)
#     return render(request, 'report_type_form.html', {'form': form})

# def report_type_delete(request, pk):
#     report_type = get_object_or_404(ReportType, pk=pk)
#     if request.method == 'POST':
#         report_type.delete()
#         return redirect('report_type_list')
#     return render(request, 'report_type_confirm_delete.html', {'report_type': report_type})
    

@login_required(login_url='/')
def report_type_list(request):
    screen_name = "Report type"
    # ========= Start filter role based data ==============
    app_name, model_name = 'accounts_reports','ReportType'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in ReportType._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('report_type_add'),
        'list_url': reverse('report_type_list'),
        'update_url': '',
        'delete_url': '',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)
    

@login_required(login_url='/')
def reportmapping_list(request):
    screen_name = "Report Mapping"
    # ========= Start filter role based data ==============
    app_name, model_name = 'accounts_reports','Reportmapping'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=True)
    # ========= End filter role based data ================
    obj_fields = [field for field in Reportmapping._meta.get_fields() if exclude_field(field.name)]

    context = {
        'obj': obj,
        'screen_name': screen_name,
        'obj_fields': obj_fields,
        'create_url': reverse('reportmapping_add'),
        'list_url': reverse('reportmapping_list'),
        'update_url': '',
        'delete_url': '',
        'is_action_required': True,
    }
    
    template_name = 'pesanile_accounting/list_everything.html'
    return render(request, template_name, context)

# def reportmapping_list(request):
#     report_mappings = Reportmapping.objects.all()
#     return render(request, 'reportmapping_list.html', {'report_mappings': report_mappings})
