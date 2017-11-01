from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from pagedown.widgets import PagedownWidget
from django.utils import timezone
from .models import Dailylog
from customers.models import Customer
from dailywork.models import Uom


class DailylogForm(forms.ModelForm):
    customer = forms.ModelChoiceField( queryset= Customer.objects.filter(invalid=False),
                                        widget= forms.Select( attrs={'class':'form-control' } ),
                                        label=('客戶') )
    work_date = forms.DateField( initial= timezone.now(),widget= forms.DateInput( attrs={'class':'form-control''vDateField' , 'onfocus':'select()', 'require':'True' } ) ,label=('工作日期'))
    start_at = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' } ),label=('出發點'),required=True )
    end_with = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' } ) ,label=('目的地') ,required=True)
    opreateDesc = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'  } ),label=('工作敘述'),required=True )
    quantity = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'  } ),label=('數量') ,required=True)
    uom = forms.ModelChoiceField( queryset= Uom.objects.all(),
                                        widget= forms.Select( attrs={'class':'form-control' } ),
                                        empty_label=None,
                                        label=('計量單位') )
    uniprice = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'   } ) ,label=('單價'),required=True)
    notes = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'    } ),label=('備註事項'),required=False)
    is_freecharge = forms.CheckboxInput()


    class Meta:
        model = Dailylog
        exclude = ('create_at','modify','invalid','payrequest', 'bill_number')






class DailylogEditForm(forms.ModelForm):
    customer = forms.ModelChoiceField( queryset= Customer.objects.filter(invalid=False),
                                        widget= forms.Select( attrs={'class':'form-control' } ),
                                        label=('客戶') )
    work_date = forms.DateField( initial= timezone.now(),widget= forms.DateInput( attrs={'class':'form-control''vDateField' , 'onfocus':'select()', 'require':'True' } ) ,label=('工作日期'))
    start_at = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' } ),label=('出發點'),required=True )
    end_with = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' } ) ,label=('目的地') ,required=True)
    opreateDesc = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'  } ),label=('工作敘述'),required=True )
    quantity = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'  } ),label=('數量') ,required=True)
    uom = forms.ModelChoiceField( queryset= Uom.objects.all(),
                                        widget= forms.Select( attrs={'class':'form-control' } ),
                                        empty_label=None,
                                        label=('計量單位') )
    uniprice = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'   } ) ,label=('單價'),required=True)
    notes = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control'    } ),label=('備註事項'),required=False)

    class Meta:
        model = Dailylog
        exclude = ('create_at','modify','bill_number')
