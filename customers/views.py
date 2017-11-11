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
    paginate_by = 15

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            query_list = Customer.objects.filter(
                Q(title__icontains=query)
            ).distinct()
            return query_list

        return Customer.objects.all()



class CustomerCreate(CreateView):
    subject = "Create New Customer"
    model = Customer
    form_class = CustomerForm
    #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
    success_url = reverse_lazy('customers:customer_list')



class CustomerUpdate(UpdateView):
    model = Customer
    form_class = CustomerEditForm
    #fields = ['title', 'unikey', 'address', 'phone', 'faxno', 'invalid']

    success_url = reverse_lazy('customers:customer_list')


class CustomerDelete(DeleteView):
    model = Customer
    #success_url = '/products'
    success_url = reverse_lazy('customers:customer_list')
