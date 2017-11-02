from django import forms
from pagedown.widgets import PagedownWidget
from .models import Customer

class CustomerForm(forms.ModelForm):
    title = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'    } ),label='客戶名稱' )
    unikey = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'  } ),label='統一編號',required=False )
    address = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'} ),label='發票地址',required=False )
    phone = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'    } ),label='聯絡電話' ,required=False)
    faxno = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'   } ),label='傳真號碼',required=False )

    class Meta:
        model = Customer
        exclude = ('create_at','modify','invalid' )


class CustomerEditForm(forms.ModelForm):
    title = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' } ),label='客戶名稱' )
    unikey = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , } ),label='統一編號',required=False )
    address = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' } ) ,label='發票地址',required=False)
    phone = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'   } ),label='聯絡電話' ,required=False )
    faxno = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'  } ),label='傳真號碼',required=False )


    class Meta:
        model = Customer
        exclude = ('create_at','modify' )
