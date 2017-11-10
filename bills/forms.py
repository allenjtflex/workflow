from django import forms
from pagedown.widgets import PagedownWidget
from .models import Bill
from customers.models import Customer
import datetime


class BillCreateForm(forms.ModelForm):
    customer = forms.CharField( widget= forms.TextInput() )
    bill_number = forms.CharField( widget= forms.TextInput(),required=False )
    ord_date = forms.CharField( widget= forms.TextInput(),required=False )

    class Meta:
        model = Bill
        exclude = ('create','updated','is_valid','paied' )


class BillEditForm(forms.ModelForm):
    customer = forms.ModelChoiceField( queryset= Customer.objects.filter(invalid=False),
                                        widget= forms.Select( attrs={'class':'form-control' } )
                                        ,label=('客戶') )
    ord_date = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control' ,'readonly':'readonly'} ) ,label=('請款日期'))
    bill_number = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control' ,'readonly':'readonly'}),label=('請款單號') )
    class Meta:
        model = Bill
        exclude = ('create','updated' )


# 自動產生請款單
first_of_month = datetime.date.today().replace(day=1)
last_of_prev_month = first_of_month - datetime.timedelta(days=1)

class BillGenerateForm(forms.Form):
    ord_date = forms.DateField( initial=last_of_prev_month, widget= forms.TextInput(attrs={'class':'form-control','onfocus':'select()' } ) ,label=('請款截止日期'))


class BatchPrintBills(forms.Form):
    start_number = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control'}),label=('從') )
    end_number = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control'}),label=('到') )
