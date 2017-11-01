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


class BillEditForm(forms.ModelForm):
    customer = forms.ModelChoiceField( queryset= Customer.objects.filter(invalid=False),
                                        widget= forms.Select( attrs={'class':'form-control' } )
                                        ,required=False
                                        ,label=('客戶') )
    ord_date = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control' ,'readonly':'readonly'} ) ,label=('請款日期'))
    bill_number = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control' ,'readonly':'readonly'}),label=('請款單號') )
    class Meta:
        model = Bill
        exclude = ('create','updated' )
