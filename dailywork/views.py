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
	ordering = ['-work_date']

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query:
			query_list = Dailylog.objects.filter(
			          Q(opreateDesc__icontains=query)|
					  Q(start_at__icontains=query)|
					  Q(end_with__icontains=query)|
					  Q(notes__icontains=query)

			)
			return query_list.order_by('-work_date')

		return Dailylog.objects.all().order_by('-work_date')





class DailylogCreate(CreateView):
    title = "Create New Dailylog"
    model = Dailylog
    form_class = DailylogForm

    #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
    success_url = reverse_lazy('dailywork:dailywork_create')



class DailylogEdit(UpdateView):
    title = "Edit New Dailylog"
    model = Dailylog
    form_class = DailylogEditForm
    #fields = ['part_number', 'description', 'specification', 'image',  'category', 'cycle_status']
    success_url = reverse_lazy('dailywork:dailywork_list')
