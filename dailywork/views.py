from django.shortcuts import render, get_object_or_404

from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
# Create your views here.

from .models import Dailylog

from .forms import DailylogForm,DailylogEditForm

class DailylogDetail(DetailView):
	model = Dailylog



class DailylogList(ListView):
	model = Dailylog
	paginate_by = 10




class DailylogCreate(CreateView):
    title = "Create New Dailylog"
    model = Dailylog
    form_class = DailylogForm
    #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
    success_url = reverse_lazy('dailywork:dailywork_list')



class DailylogEdit(UpdateView):
    title = "Edit New Dailylog"
    model = Dailylog
    form_class = DailylogEditForm
    #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
    success_url = reverse_lazy('dailywork:dailywork_list')
