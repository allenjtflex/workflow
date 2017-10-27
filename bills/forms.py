from django import forms
from pagedown.widgets import PagedownWidget
from .models import Bill
from customers.models import Customer



class BillCreateForm(forms.ModelForm):
    customer = forms.CharField( widget= forms.TextInput() )
    bill_number = forms.CharField( widget= forms.TextInput(),required=False )
    ord_date = forms.CharField( widget= forms.TextInput(),required=False )


    class Meta:
        model = Bill
        exclude = ('create','updated','is_valid' )
