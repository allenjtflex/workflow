from django.conf.urls import url
from django.contrib import admin

from .views import DailylogList, DailylogDetail

urlpatterns = [

    url(r'^$', DailylogList.as_view( template_name ='dailywork/dailylog_list.html') ),
    url(r'^(?P<pk>\d+)/$', DailylogDetail.as_view( template_name ='dailywork/dailylog_detail.html'), name="detail"  ),

]
