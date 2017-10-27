from django.contrib import admin
from . import models

# Register your models here.

class DailylogAdmin(admin.ModelAdmin):
    list_display = ( 'work_date', 'customer', 'opreateDesc', 'start_at', 'end_with', 'notes', 'payrequest', 'bill_number' )
    list_display_links = ( 'work_date', 'customer', 'opreateDesc',)
    list_per_page = 10
    #search_fields = ['title']



admin.site.register(models.Uom)

admin.site.register(models.Dailylog, DailylogAdmin)
