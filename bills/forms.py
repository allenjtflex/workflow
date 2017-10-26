from django import forms
from pagedown.widgets import PagedownWidget
from .models import Bill
from customers.models import Customer



class BillCreateForm(forms.ModelForm):
    # # customer = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'客戶名稱'  } ) )
    # bill_number = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'統一編號'  } ),required=False )
    # ord_date = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control', 'size':'30',  'placeholder':'發票地址' } ),required=False )


    class Meta:
        model = Bill
        exclude = ('create','updated','is_valid' )
