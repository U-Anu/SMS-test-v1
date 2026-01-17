from django import forms
from pesanile_accounting.models import *


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        # fields = ('first_name', 'last_name', 'email', 'phone_number', 'company_name', 'password',)
        exclude = ('company_name','branch_name','is_staff', 'is_active', 'user_permissions', 'groups', 'is_superuser', 'is_customer', 'last_login',)
        # fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','middle_name','last_name','email','phone_number','password']
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
