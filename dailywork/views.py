from django.shortcuts import render, get_object_or_404

from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q
# Create your views here.

from .models import Dailylog


class DailylogDetail(DetailView):

	model = Dailylog



class DailylogList(ListView):

	model = Dailylog