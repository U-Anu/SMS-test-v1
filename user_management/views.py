from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from pesanile_accounting.models import Company, User, Branch
from pesanile_accounting.check_permission import check_user_role_return_db


@login_required(login_url='user_login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='user_login')
def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            branch_name = request.POST.get('branch_name')
            print('branch_name ',branch_name)
            obj.company_name = request.user.company_name
            obj.branch_name_id = branch_name
            obj.password = make_password(form.cleaned_data.get('password'))
            obj.save()
            return redirect('user_list')  # Redirect to a success page after registration
    else:
        branch_obj = Branch.objects.filter(created_by_id=request.user.pk)
        form = UserRegistrationForm()
    print('branch_obj ',branch_obj)
    context = {
        'form': form, 'user_registration': 'active', 'user_registration_show': 'show',
        'branch_obj':branch_obj,
    }
    return render(request, 'UserManagement/user_registration.html', context)


def user_login(request):
    if request.method == 'POST':
        print('request.POST', request.POST)
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            print('user ',user)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to a success page
            else:
                print('Invalid username or password')
                form.add_error(None, 'Invalid username or password')
        else:
            print('form', form.errors)
    else:
        form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'Auth/login.html', context)


def user_list(request):
    # records = User.objects.all()
    # ========= Start filter role based data ==============
    app_name, model_name = 'pesanile_accounting','User'
    obj = check_user_role_return_db(app_name, model_name, request, list_all=False)
    # ========= End filter role based data ================
    context = {
        'user_list': 'active', 'user_list_show': 'show', 'records': obj
    }
    return render(request, 'UserManagement/user_list.html', context)


def maker_checker_mapping(request):
    if request.method == 'POST':
        print('request.POST', request.POST)
        form = MakerCheckerMappingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('maker_checker_mapping_list')
        else:
            print('form', form.errors)
    else:
        form = MakerCheckerMappingForm()

    context = {
        'form': form, 'maker_checker_mapping': 'active', 'maker_checker_mapping_show': 'show',
    }
    return render(request, 'UserManagement/maker_checker_mapping.html', context)


def maker_checker_mapping_list(request):
    records = MakerCheckerMapping.objects.all()
    context = {
        'maker_checker_mapping': 'active', 'maker_checker_mapping_show': 'show', 'records': records
    }
    return render(request, 'UserManagement/maker_checker_mapping_list.html', context)

@login_required(login_url='user_login')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('user_login')
    else:
        return redirect('user_login')


def signup_views(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.is_customer=True
            obj.password = make_password(form.cleaned_data.get('password'))
            obj.save()# save the user with hashed password
            com_obj = Company.objects.create(created_by=obj) # create the company
            obj.company_name=com_obj # update company id
            obj.save()
            print('com_obj ',com_obj)
            return redirect('dashboard')  # Redirect to a success page after registration
    else:
        form = SignUpForm()

    context = {
        'form': form, 'signup': 'active', 'signup_show': 'show',
    }
    return render(request, 'UserManagement/signup.html', context)
