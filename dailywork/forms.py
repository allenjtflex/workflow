from django import forms
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from pagedown.widgets import PagedownWidget
from django.utils import timezone
from .models import Dailylog


class DailylogForm(forms.ModelForm):
    work_date = forms.DateField( initial= timezone.now(),widget= forms.DateInput( attrs={'class':'form-control''vDateField' , 'onfocus':'select()', 'require':'True' } ) ,label=('工作日期'))
    start_at = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control', 'size':'30',  'placeholder':'出發點' } ),label=('出發點'),required=False )
    end_with = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'目的地'  } ) ,required=False)
    opreateDesc = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'工作敘述'  } ),required=False )
    quantity = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'數量'  } ) ,required=False)
    #uom = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'單位'  } ) ,required=False)
    uniprice = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'單價'  } ) ,required=False)
    notes = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'備註事項'  } ),required=False)

    class Meta:
        model = Dailylog
        exclude = ('create_at','modify','invalid','payrequest ', 'bill_number')
        widgets = {
            'customer': forms.Select(attrs={ 'class':'form-control'}),
            'uom': forms.Select(attrs={ 'class':'form-control'}),
        }


class DailylogEditForm(forms.ModelForm):
    work_date = forms.DateField( initial= timezone.now(),widget= forms.DateInput( attrs={'class':'form-control''vDateField' , 'onfocus':'select()', 'require':'True' } ) ,label=('工作日期'))
    start_at = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control', 'size':'30',  'placeholder':'出發點' } ),label=('出發點'),required=False )
    end_with = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'目的地'  } ) ,required=False)
    opreateDesc = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'工作敘述'  } ),required=False )
    quantity = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'數量'  } ) ,required=False)
    #uom = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'單位'  } ) ,required=False)
    uniprice = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'單價'  } ) ,required=False)
    notes = forms.CharField( widget= forms.TextInput( attrs={'class':'form-control' , 'size':'30' , 'placeholder':'備註事項'  } ),required=False)

    class Meta:
        model = Dailylog
        exclude = ('create_at','modify','invalid','payrequest ', 'bill_number')
        widgets = {
            'customer': forms.Select(attrs={ 'class':'form-control'}),
            'uom': forms.Select(attrs={ 'class':'form-control'}),
        }
