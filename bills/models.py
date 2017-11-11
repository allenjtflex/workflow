from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
from customers.models import Customer
from dailywork.models import Dailylog
import datetime



# class BillQueryset(models.query.QuerySet):
#
# 	# 未請款的項目
# 	def get_effective(self):
# 		return self.filter( is_valid= True  )
first_of_month = datetime.date.today().replace(day=1)
last_of_prev_month = first_of_month - datetime.timedelta(days=1)




#自訂單據號碼
class BillNumberManager(models.Manager):


    #短的月份序號如：16080001
    def short_month_sequence(self):
        order_date = str(datetime.date.today())
        nextNumber = self.filter(created__contains = order_date[:7] ).count()+1
        bill_number = nextNumber + int(order_date[2:7].replace('-',''))*10000
        return bill_number
    #月份序號如：2016080001
    def month_sequence( self, dutydate=None ):

        order_date = str(datetime.date.today())

        if dutydate is not None:
            order_date = dutydate
        #
        #
        #
        # # if args is not None:
        #     order_date = str(args)


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
    #
    # def get_queryset(self):
    #     return BillQueryset(self.model, using=self.db)
    #
    #
    # def get_effective(self):
    #     return self.query_set().get_effective()


class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=12, null=True, blank=True, unique=True)
    ord_date = models.DateField(default=timezone.now) #請款日期
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = BillNumberManager()
    is_valid = models.BooleanField(default=False, verbose_name="單據作廢")# True代表此單據作廢
    paied = models.BooleanField(default=False,verbose_name="已付款")# True代表此單據已付款

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Bill {}'.format(self.id)

    def get_total_amount(self):
        total =  sum( int(obj.item.get_amount()) for obj in self.billitem_set.all())
        return total

    def get_tax_amount(self):
        return int(float(self.get_total_amount()) * 0.05)

    def get_grand_amount(self):
        return sum( (self.get_total_amount(), self.get_tax_amount()))


    def get_absolute_url(self):
        return reverse('bills:bill_detail', kwargs={"pk": self.id} )

    # def get_effective(self):
    #     return self.filter( is_valid__exact=1  )



class BillItem(models.Model):
    bill = models.ForeignKey(Bill)
    item = models.ForeignKey(Dailylog,  on_delete=models.CASCADE,related_name='bill_items')


    class Meta:
        ordering = ( 'item', )

    def __str__(self):
        return '{}'.format(self.id)

    def get_item_amount(self):
        return self.uniprice * self.quantity


    def get_absolute_url(self):
        return reverse('bills:bill_detail',args=[self.id])
