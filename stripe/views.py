# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.base import TemplateView
from .models import Sample, Car
from django.shortcuts import render, redirect
from django.conf import settings

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):  # new
        context = super(TemplateView, self, **kwargs).get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


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