from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from .forms import *
from .scripts import *
from .account_entries import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .scripts_pr import apply_payment_to_payable, apply_payment_to_receivable, get_receivable_and_payable_details
from django.http import HttpResponseRedirect
import datetime
import random

from .models import *
from datetime import date
from django.utils.crypto import get_random_string
from .tenant_ways import tenant_create_save,pre_setup_tenant_create_save
from .check_permission import check_user_role_return_db

def error_500(request):
    template_name='500.html'
    exception_error = request.session.get('exception_error')
    context = {
        'exception_error':exception_error
    }
    return render(request, template_name,context)

# Branch Update View
@login_required(login_url='user_login')
def branch_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(Branch, pk=pk)
        if request.method == 'POST':
            form = BranchForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('branch_list')
        else:
            form = BranchForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('branch_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def branch_delete(request,pk):
    try:
        obj = get_object_or_404(Branch, pk=pk)
        obj.delete()
        return redirect('branch_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Branch Update View
@login_required(login_url='user_login')
def company_update(request,pk):
    try:
        obj = get_object_or_404(Company, pk=pk)
        if request.method == 'POST':
            form = CompanyForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('company_list')
        else:
            form = CompanyForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('company_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def company_delete(request,pk):
    try:
        obj = get_object_or_404(Company, pk=pk)
        obj.delete()
        return redirect('company_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Branch Update View
@login_required(login_url='user_login')
def currency_update(request,pk):
    try:
        obj = get_object_or_404(Currency, pk=pk)
        if request.method == 'POST':
            form = CurrencyForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('currency_list')
        else:
            form = CurrencyForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('currency_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Delete View
@login_required(login_url='user_login')
def currency_delete(request,pk):
    try:
        obj = get_object_or_404(Currency, pk=pk)
        obj.delete()
        return redirect('currency_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Branch Update View
@login_required(login_url='user_login')
def asset_type_update(request,pk):
    try:
        obj = get_object_or_404(AssetType, pk=pk)
        if request.method == 'POST':
            form = AssetTypeForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('asset_type_list')
        else:
            form = AssetTypeForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('asset_type_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def asset_type_delete(request,pk):
    try:
        obj = get_object_or_404(AssetType, pk=pk)
        obj.delete()
        return redirect('asset_type_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Branch Update View
@login_required(login_url='user_login')
def glline_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(GLLine, pk=pk)
        if request.method == 'POST':
            form = GLLineForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('glline_list')
        else:
            form = GLLineForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('glline_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def glline_delete(request,pk):
    try:
        obj = get_object_or_404(GLLine, pk=pk)
        obj.delete()
        return redirect('glline_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Branch Update View
@login_required(login_url='user_login')
def transaction_code_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(TransactionCode, pk=pk)
        if request.method == 'POST':
            form = TransactionCodeForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('transaction_code_list')
        else:
            form = TransactionCodeForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('transaction_code_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def transaction_code_delete(request,pk):
    try:
        obj = get_object_or_404(TransactionCode, pk=pk)
        obj.delete()
        return redirect('transaction_code_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Branch Update View
@login_required(login_url='user_login')
def transaction_type_classification_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(TransactionTypeClassification, pk=pk)
        if request.method == 'POST':
            form = TransactionTypeClassificationForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('transaction_type_classification_list')
        else:
            form = TransactionTypeClassificationForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('transaction_type_classification_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def transaction_type_classification_delete(request,pk):
    try:
        obj = get_object_or_404(TransactionTypeClassification, pk=pk)
        obj.delete()
        return redirect('transaction_type_classification_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Branch Update View
@login_required(login_url='user_login')
def branch_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(Branch, pk=pk)
        if request.method == 'POST':
            form = BranchForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('branch_list')
        else:
            form = BranchForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('branch_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def branch_delete(request,pk):
    try:
        obj = get_object_or_404(Branch, pk=pk)
        obj.delete()
        return redirect('branch_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Update View
@login_required(login_url='user_login')
def branch_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(Branch, pk=pk)
        if request.method == 'POST':
            form = BranchForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('branch_list')
        else:
            form = BranchForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('branch_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def branch_delete(request,pk):
    try:
        obj = get_object_or_404(Branch, pk=pk)
        obj.delete()
        return redirect('branch_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Update View
@login_required(login_url='user_login')
def branch_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(Branch, pk=pk)
        if request.method == 'POST':
            form = BranchForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('branch_list')
        else:
            form = BranchForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('branch_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def branch_delete(request,pk):
    try:
        obj = get_object_or_404(Branch, pk=pk)
        obj.delete()
        return redirect('branch_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Update View
@login_required(login_url='user_login')
def transaction_type_mode_update(request,pk):
    try:
        obj = get_object_or_404(TransactionTypeMode, pk=pk)
        if request.method == 'POST':
            form = TransactionTypeModeForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('transaction_type_mode_list')
        else:
            form = TransactionTypeModeForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('transaction_type_mode_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Branch Delete View
@login_required(login_url='user_login')
def transaction_type_mode_delete(request,pk):
    try:
        obj = get_object_or_404(TransactionTypeMode, pk=pk)
        obj.delete()
        return redirect('transaction_type_mode_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Update View
@login_required(login_url='user_login')
def account_category_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(AccountCategory, pk=pk)
        if request.method == 'POST':
            form = AccountCategoryForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('account_category_list')
        else:
            form = AccountCategoryForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('account_category_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Delete View
@login_required(login_url='user_login')
def account_category_delete(request,pk):
    try:
        obj = get_object_or_404(AccountCategory, pk=pk)
        obj.delete()
        return redirect('account_category_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Account Category Update View
@login_required(login_url='user_login')
def account_restriction_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(AccountRestriction, pk=pk)
        if request.method == 'POST':
            form = AccountRestrictionForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('account_restriction_list')
        else:
            form = AccountRestrictionForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('account_restriction_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Delete View
@login_required(login_url='user_login')
def account_restriction_delete(request,pk):
    try:
        obj = get_object_or_404(AccountRestriction, pk=pk)
        obj.delete()
        return redirect('account_restriction_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Account Category Update View
@login_required(login_url='user_login')
def account_type_category_update(request,pk):
    try:
        obj = get_object_or_404(AccountTypeCategory, pk=pk)
        if request.method == 'POST':
            form = AccountTypeCategoryForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('account_type_category_list')
        else:
            form = AccountTypeCategoryForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('account_type_category_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Delete View
@login_required(login_url='user_login')
def account_type_category_delete(request,pk):
    try:
        obj = get_object_or_404(AccountTypeCategory, pk=pk)
        obj.delete()
        return redirect('account_type_category_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Account Category Update View
@login_required(login_url='user_login')
def account_type_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(AccountType, pk=pk)
        if request.method == 'POST':
            form = AccountTypeForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('account_type_list')
        else:
            form = AccountTypeForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('account_type_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Delete View
@login_required(login_url='user_login')
def account_type_delete(request,pk):
    try:
        obj = get_object_or_404(AccountType, pk=pk)
        obj.delete()
        return redirect('account_type_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Account Update View
@login_required(login_url='user_login')
def account_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(Accounts, pk=pk)
        if request.method == 'POST':
            form = AccountForm(request.POST, instance=obj,created_by=request.user)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('account_list')
        else:
            form = AccountForm(instance=obj,created_by=request.user)
        context = {
            'form' : form,
            'list_url': reverse('account_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Delete View
@login_required(login_url='user_login')
def account_delete(request,pk):
    try:
        obj = get_object_or_404(Accounts, pk=pk)
        obj.delete()
        return redirect('account_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Account Category Update View
@login_required(login_url='user_login')
def reference_type_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(ReferenceType, pk=pk)
        if request.method == 'POST':
            form = ReferenceTypeForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('reference_type_list')
        else:
            form = ReferenceTypeForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('reference_type_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Delete View
@login_required(login_url='user_login')
def reference_type_delete(request,pk):
    try:
        obj = get_object_or_404(ReferenceType, pk=pk)
        obj.delete()
        return redirect('reference_type_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Account Category Update View
@login_required(login_url='user_login')
def payment_complexity_update(request,pk):
    try:
        obj = get_object_or_404(PaymentComplexity, pk=pk)
        if request.method == 'POST':
            form = PaymentComplexityForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('payment_complexity_list')
        else:
            form = PaymentComplexityForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('payment_complexity_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Delete View
@login_required(login_url='user_login')
def payment_complexity_delete(request,pk):
    try:
        obj = get_object_or_404(PaymentComplexity, pk=pk)
        obj.delete()
        return redirect('payment_complexity_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')


# Account Category Update View
@login_required(login_url='user_login')
def account_category_update(request,pk):
    try:
        print('pk ',pk)
        obj = get_object_or_404(AccountCategory, pk=pk)
        if request.method == 'POST':
            form = AccountCategoryForm(request.POST, instance=obj)
            if form.is_valid():
                # =========== Update =================
                form_obj = form.save(commit=False)
                form_obj.updated_by=request.user
                form_obj.save()
                # =========== Update =================
                return redirect('account_category_list')
        else:
            form = AccountCategoryForm(instance=obj)
        context = {
            'form' : form,
            'list_url': reverse('account_category_list'),
        }
        return render(request, 'pesanile_accounting/create_everything.html', context)
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

# Account Category Delete View
@login_required(login_url='user_login')
def account_category_delete(request,pk):
    try:
        obj = get_object_or_404(AccountCategory, pk=pk)
        obj.delete()
        return redirect('account_category_list')
    except Exception as error:
        request.session['exception_error'] = f"""{error}"""
        return redirect('error_500')

