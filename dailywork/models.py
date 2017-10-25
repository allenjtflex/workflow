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

	def paied(self):
		return self.filter(payrequest=False)



class DailylogManager(models.Manager):

	def get_queryset(self):
		return DailylogQueryset(self.model, using=self.db)

	def paied(self, *args, **kwargs):
		return self.query_set().paied()






class Dailylog(models.Model):

	work_date = models.DateField( default=timezone.now )
	customer = models.ForeignKey(Customer)
	start_at = models.CharField(  max_length=20, null=False, blank=False )
	end_with = models.CharField(  max_length=20, null=False, blank=False )
	opreateDesc = models.CharField(max_length=30, blank=False, null=False)
	quantity = models.DecimalField( max_digits=10, decimal_places=0)
	uom = models.ForeignKey(Uom)
	uniprice = models.DecimalField( max_digits=10, decimal_places=0)
	notes = models.TextField(blank=True, null=True)

	payrequest = models.BooleanField(default=False)    # 是否已請款
	bill_number = models.CharField(  max_length=20, null=True, blank=True )
	invalid = models.BooleanField(default=False)
	create_at = models.DateTimeField( auto_now_add=True, auto_now=False)
	modify = models.DateTimeField( auto_now_add=False, auto_now=True)

	objects = DailylogManager()

	def __str__(self):
		return self.opreateDesc
	
	def get_absolute_url(self):
		return reverse( "dailywork:dailywork_edit", kwargs={"pk": self.pk} )

	def get_amount(self):
		return self.quantity * self.uniprice
