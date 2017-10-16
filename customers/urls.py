from django.conf.urls import url
from django.contrib import admin


from .views import CustomerList, CustomerDetail,CustomerCreate,CustomerUpdate
urlpatterns = [

    url(r'^$', CustomerList.as_view( template_name ='customers/customer_list.html') , name="customer_list" ),
    url(r'^(?P<pk>\d+)/$', CustomerDetail.as_view( template_name ='customers/customer_detail.html'), name="customer_detail"  ),
    url(r'^create/$', CustomerCreate.as_view( template_name = 'customers/customer_form.html' ), name="customer_create" ),
    url(r'^(?P<pk>\d+)/edit/$', CustomerUpdate.as_view( template_name = 'customers/customer_form.html' ), name="customer_edit" ),


]
