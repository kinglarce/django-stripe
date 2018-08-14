# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Sample, Car

# Register your models here.
admin.site.register([Sample, Car])