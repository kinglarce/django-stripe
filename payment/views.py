# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.base import TemplateView
from .models import Sample, Car
from django.shortcuts import render, redirect, render_to_response
from django.conf import settings

from django.http import HttpResponse
from django.template import RequestContext

from .models import Sale
from .forms import SalePaymentForm

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):  # new
        context = super(IndexView, self).get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):
    if request.method == "POST":
        form = SalePaymentForm(request.POST)

        if form.is_valid():  # charges the card
            return HttpResponse("Success! We've charged your card!")
    else:
        form = SalePaymentForm()

    return render_to_response("charge.html", RequestContext(request, {'form': form}))


# def payment_form(request):
#     context = {"stripe_key": settings.STRIPE_PUBLISHABLE_KEY}
#     return render(request, "payment_form.html", context)

#
# def checkout(request):
#     new_car = Car(
#         model="Honda Civic",
#         year=2017
#     )
#
#     if request.method == "POST":
#         token = request.POST.get("stripeToken")
#
#     try:
#         charge = stripe.Charge.create(
#             amount=2000,
#             currency="usd",
#             source=token,
#             description="The product charged to the user"
#         )
#
#         new_car.charge_id = charge.id
#
#     except stripe.error.CardError as ce:
#         return False, ce
#
#     else:
#         new_car.save()
#         return redirect("success")
#         # The payment was successfully processed, the user's card was charged.
#         # You can now redirect the user to another page or whatever you want
#
class SuccessView(TemplateView):
    template_name = 'success.html'
