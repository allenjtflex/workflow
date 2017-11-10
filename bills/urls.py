from django.conf.urls import url
from django.contrib import admin
from . import views


from .views import BillList, BillDetail, BillUpdate
urlpatterns = [

    url(r'^$', BillList.as_view( template_name ='bills/bill_list.html') , name="bill_list" ),
    url(r'^(?P<pk>\d+)/$', BillDetail.as_view( template_name ='bills/bill_detail.html'), name="bill_detail"  ),
    # url(r'^create/$', CustomerCreate.as_view( template_name = 'customers/customer_form.html' ), name="customer_create" ),
    url(r'^(?P<pk>\d+)/edit/$', BillUpdate.as_view( template_name = 'bills/bill_form.html' ), name="bill_edit" ),

    url(r'^(?P<id>\d+)/deleteitem/$', views.billitem_delete ),
    url(r'^checkout/(?P<id>\d+)/$', views.bill_create ),
    url(r'^bill_genegerate/$', views.generate_bill, name="genegerate_bills" ),
    url(r'^print_bills/$', views.print_bills, name="print_bills" ),

    url(r'^(?P<id>\d+)/gen_pdfv2/$', views.gen_pdfv2 , name="gen_pdfv2" ),


]
