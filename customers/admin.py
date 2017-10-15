from django.contrib import admin
from . import models
# Register your models here.

class CustomerAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'unikey', 'address','phone','faxno')
    list_display_links = ( 'title', 'phone',)
    list_per_page = 10
    search_fields = ['title']


admin.site.register( models.Customer, CustomerAdmin )