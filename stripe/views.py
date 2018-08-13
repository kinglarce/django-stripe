# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views import generic
from .models import Sample
from django.shortcuts import render

# Create your views here.

class IndexView(generic.ListView):
    template_name = 'index.html'

    def get_queryset(self):
        return Sample.objects.all()