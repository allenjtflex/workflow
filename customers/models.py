from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.

#客戶
class Customer(models.Model):

    title = models.CharField(max_length=36, null=False, blank=False, verbose_name='客戶名稱')
    unikey = models.CharField(  max_length=12,null=True, blank=True, verbose_name='統一編號' )
    address = models.CharField( max_length=100, null=True, blank=True, verbose_name='地址')

    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='電話')
    faxno = models.CharField(max_length=20, null=True, blank=True, verbose_name='傳真')

    invalid = models.BooleanField(default=False, verbose_name='停用')

    create_at = models.DateTimeField(auto_now_add=True, auto_now =False)
    modify = models.DateTimeField(auto_now_add=False, auto_now =True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse( "customers:customer_detail", kwargs={"pk": self.pk} )
