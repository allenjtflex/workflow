from django.conf.urls import url
from django.contrib import admin


from .views import CustomerList, CustomerDetail
urlpatterns = [

    #url(r'^dailyworks/', include( 'customers.urls', namespace="customers")),
    url(r'^$', CustomerList.as_view( template_name ='customers/customer_list.html') ),
    url(r'^(?P<pk>\d+)/$', CustomerDetail.as_view( template_name ='customers/customer_detail.html'), name="customer_detail"  ),

]
