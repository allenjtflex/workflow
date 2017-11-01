from django.db import models

from django.utils import timezone
from django.core.urlresolvers import reverse

from customers.models import Customer

# Create your models here.
class Uom(models.Model):
	descriotion =  models.CharField(  max_length=20, null=False, blank=False )

	def __str__(self):
		return self.descriotion


class DailylogQueryset(models.query.QuerySet):

	# 未請款的項目
	def norequest(self):
		return self.filter(payrequest=False , is_freecharge=False , invalid= False  )



class DailylogManager(models.Manager):

	def get_queryset(self):
		return DailylogQueryset(self.model, using=self.db)

	# 未請款的項目
	def norequest(self, *args, **kwargs):
		return self.query_set().norequest()



class Dailylog(models.Model):

	work_date = models.DateField( default=timezone.now )
	customer = models.ForeignKey(Customer)
	start_at = models.CharField(  max_length=20, null=False, blank=False )
	end_with = models.CharField(  max_length=20, null=False, blank=False )
	opreateDesc = models.CharField(max_length=20, blank=False, null=False)
	quantity = models.DecimalField( max_digits=10, decimal_places=0)
	uom = models.ForeignKey(Uom)
	uniprice = models.DecimalField( max_digits=10, decimal_places=0)
	notes = models.TextField(blank=True, null=True)

	payrequest = models.BooleanField(default=False, verbose_name='已請款')    # 是否已請款
	is_freecharge = models.BooleanField(default=False, verbose_name='免費項目')    # 是否爲免費項目, 如果為免費項目則在未請款清單是不會顯示的
	bill_number = models.CharField(  max_length=20, null=True, blank=True )
	invalid = models.BooleanField(default=False, verbose_name='項目作廢')
	create_at = models.DateTimeField( auto_now_add=True, auto_now=False)
	modify = models.DateTimeField( auto_now_add=False, auto_now=True)

	objects = DailylogManager()

	def __str__(self):
		return self.opreateDesc

	def get_absolute_url(self):
		return reverse( "dailywork:dailywork_edit", kwargs={"pk": self.pk} )

	def get_amount(self):
		return self.quantity * self.uniprice
