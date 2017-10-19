from django.conf.urls import url
from django.contrib import admin

from .views import DailylogList, DailylogDetail, DailylogCreate,DailylogEdit

urlpatterns = [

    url(r'^$', DailylogList.as_view( template_name ='dailywork/dailylog_list.html') , name="dailywork_list" ),
    url(r'^(?P<pk>\d+)/$', DailylogEdit.as_view( template_name ='dailywork/dailylog_form.html'), name="dailywork_edit"  ),
    #url(r'^(?P<pk>\d+)/$', DailylogDetail.as_view( template_name ='dailywork/dailylog_detail.html'), name="dailywork_detail"  ),
    url(r'^create/$', DailylogCreate.as_view( template_name ='dailywork/dailylog_form.html'), name="dailywork_create"  ),

]
