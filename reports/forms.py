from django import forms
from pesanile_accounting.models import Accounts, TransactionCode,  GLLine
from sub_part.models import User,Company,Branch

class DateWiseForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Start Date',
        help_text='Select the start date for the range.',
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='End Date',
        help_text='Select the end date for the range.',
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                self.add_error('end_date', 'End date must be greater than or equal to the start date.')
        return cleaned_data


class TransactionIdForm(forms.Form):
    transaction_id = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Enter the transaction ID.',
        required=True
    )


class AccountWiseReportForm(forms.Form):
    account_number = forms.ChoiceField(choices=[],
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['account_number'].choices = [('', 'Select an Account')] + [(account.pk, account.account_number) for account in
                                                    Accounts.objects.all()]


class TellerWiseReportForm(forms.Form):
    teller = forms.ChoiceField(choices=[],
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teller'].choices= [('', 'Select an Teller/User')] + [(user.pk, user.first_name) for user in
                                                       User.objects.all()]



class TransactionCodeWiseReportForm(forms.Form):
    transaction_code = forms.ChoiceField(choices=[],
                                         widget=forms.Select(attrs={'class': 'form-control'}),
                                         )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['transaction_code'].choices = [('', 'Select an Transaction code')] + [(data.pk, data.name) for data in
                                                          TransactionCode.objects.all()]


class CompanyWiseReportForm(forms.Form):
    company = forms.ChoiceField(choices='',
                                widget=forms.Select(attrs={'class': 'form-control'}),
                                )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = [('', 'Select an Company')] + [(data.pk, data.company_name) for data in
                                                 Company.objects.all()]


class TrailBalanceReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Start Date',
        help_text='Select the start date for the range.',
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='End Date',
        help_text='Select the end date for the range.',
        required=True
    )


class GLLineReportForm(forms.Form):
    glline = forms.ChoiceField(choices=[],
                               widget=forms.Select(attrs={'class': 'form-control'}),
                               )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Start Date',
        help_text='Select the start date for the range.',
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='End Date',
        help_text='Select the end date for the range.',
        required=True
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['company'].choices = [('', 'Select an GL Line')] + [(data.pk, data.gl_line_number) for data in
                                                   GLLine.objects.all()]
