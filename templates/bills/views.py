from django.shortcuts import render, get_object_or_404

from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q

# Create your views here.
from .models import Customer
from .forms import CustomerForm,CustomerEditForm


class CustomerDetail(DetailView):
    model = Customer



class CustomerList(ListView):
    model = Customer



class CustomerCreate(CreateView):
    title = "Create New Customer"
    model = Customer
    form_class = CustomerForm
    #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
    success_url = reverse_lazy('customers:customer_list')



class CustomerUpdate(UpdateView):
    model = Customer
    form_class = CustomerEditForm
    #fields = ['title', 'unikey', 'address', 'phone', 'faxno', 'invalid']

    success_url = reverse_lazy('customers:customer_list') #因為不會回到該項資料的Detail, 所以先回到List吧


class CustomerDelete(DeleteView):
    model = Customer
    #success_url = '/products'
    success_url = reverse_lazy('customers:customer_list')
