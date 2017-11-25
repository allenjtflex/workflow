
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import views
from django.contrib import auth
from django.contrib.auth.views import login, logout
from django.contrib.auth.decorators import login_required

from django.views.generic.detail import  DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models import Q

from bills.models import Bill


def index(request):
    title="Mysite Home"
    #return HttpResponse("<h1>%s</h1>" %(title))
    return render( request, 'index.html', locals() )


class IndexList(ListView):


    def get_queryset(self, *args, **kwargs):

        query_set = Bill.objects.all()

        return query_set
