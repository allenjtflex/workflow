from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
from customers.models import Customer
from dailywork.models import Dailylog


#自訂單據號碼
class BillNumberManager(models.Manager):

    #短的月份序號如：16080001
    def short_month_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date[:7] ).count()+1
        bill_number = nextNumber + int(order_date[2:7].replace('-',''))*10000
        return bill_number
    #月份序號如：2016080001
    def month_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date[:7] ).count()+1
        bill_number = nextNumber + int(order_date[:7].replace('-',''))*10000
        return bill_number
    #月份序號如：2016080001
    def day_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date ).count()+1
        bill_number = nextNumber + int(order_date.replace('-',''))*10000
        return bill_number
    #短的日序號如：1608310001
    def short_day_sequence(self):
        order_date, _ = str(timezone.now()).split(' ')
        nextNumber = self.filter(created__contains = order_date ).count()+1
        bill_number = nextNumber + int(order_date.replace('-','')[2:])*10000
        return bill_number


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=12, null=True, blank=True, unique=True) 
    ord_date = models.DateField(default=timezone.now) #請款日期
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = BillNumberManager()
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Bill {}'.format(self.id)

    # def get_total_cost(self):
    #     return sum(item.get_cost() for item in self.items.all())


    def get_absolute_url(self):
        return reverse('bills:bill_detail', kwargs={"pk": self.id} )



class BillItem(models.Model):
    bill = models.ForeignKey(Bill)
    item = models.ForeignKey(Dailylog,  related_name='bill_items')


    class Meta:
        ordering = ( 'item', )



    def __str__(self):
        return '{}'.format(self.id)

    # def get_cost(self):
    #     return self.price * self.quantity


    def get_absolute_url(self):
        return reverse('bills:bill_detail',args=[self.id])
