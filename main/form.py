from django import forms
from .models import Client, Loan


class MainForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        super(MainForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.required = True
        



class ClientForm(MainForm):

    class Meta:

        model = Client
        fields = '__all__'

class LoanForm(MainForm):

    class Meta:

        model = Loan
        fields = '__all__'


class SendSMSForm(forms.Form):
    phone_number = forms.CharField(max_length=10)
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 3, 'rows': 3}))

    def __init__(self, initial_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].initial = initial_data.get('phone_number', '')
        self.fields['message'].initial = initial_data.get('message', '')
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
