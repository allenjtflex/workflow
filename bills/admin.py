from django.contrib import admin

# Register your models here.
from .models import Bill, BillItem



class BillItemInline(admin.TabularInline):
    model = BillItem
    raw_id_fields = ['item']



class BillAdmin(admin.ModelAdmin):

    list_display = [ 'is_valid','customer']
    list_display_links = ['customer']
    raw_id_fields = ['customer']
    list_filter = ['is_valid']
    inlines = [BillItemInline]

admin.site.register(Bill, BillAdmin)
