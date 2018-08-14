# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.base import TemplateView
from .models import Sample, Car
from django.shortcuts import render, redirect, render_to_response
from django.conf import settings

from django.http import HttpResponse
from django.template import RequestContext

# from django.urls import reverse

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


def payment_form(request):
    context = {"stripe_key": settings.STRIPE_PUBLISHABLE_KEY}
    return render(request, "payment_form.html", context)


def checkout(request):
    new_car = Car(
        name="Toyota",
        year=2017
    )

    """
    Transaction need to be recorded:
    plan, user profile, order id / charge id, amount, is ordered, data ordered = date time now, customer id
    """

    if request.method == "POST":
        token = request.POST.get("stripeToken")
        email = request.POST.get("stripeEmail")
        plan_id = request.POST.get("paymentPlanId")
        plan_name = request.POST.get("paymentPlanName")

    try:
        customer = stripe.Customer.create(
            source=token,
            email=email,
        )

        # charge on the spot
        # charge = stripe.Charge.create(
        #     amount=999,
        #     currency='eur',
        #     description='Example charge',
        #     # source=token,
        #     customer=customer.id,
        # )

        # every thirty day
        # plan = stripe.Plan.create(
        #     nickname=prod_name,
        #     product=prod_id,
        #     amount=amount,
        #     currency="eur",
        #     interval="month",
        #     usage_type="licensed",
        # )

        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[
                {
                    "plan": plan_id,
                    "quantity": 1,
                },
            ]
        )

        # subscription = stripe.Subscription.create(
        #     customer=customer.id,
        #     items=[{'plan': 'plan_CBb6IXqvTLXp3f'}],
        #     billing='send_invoice',
        #     days_until_due=30,
        # )

        # subscription = stripe.Subscription.create(
        #     customer=customer.id,
        #     items=[{'plan': 'prod_Cx3xoJJU5yOMTv'}],
        # )

        new_car.charge_id = ''
        new_car.plan_id = plan_id
        new_car.subscription_id = subscription.id
        new_car.customer_id = customer.id

    except stripe.error.CardError as ce:
        return False, ce

    else:
        new_car.save()
        return redirect("success")
        # The payment was successfully processed, the user's card was charged.
        # You can now redirect the user to another page or whatever you want


class SuccessView(TemplateView):
    template_name = 'success.html'

#
# def checkoutv2(request):
#     publishKey = settings.STRIPE_PUBLISHABLE_KEY
#     if request.method == 'POST':
#         try:
#             token = request.POST['stripeToken']
#
#             charge = stripe.Charge.create(
#                 amount=900,
#                 currency='usd',
#                 description='Example charge',
#                 source=token,
#             )
#             return redirect(reverse('shopping_cart:update_records',
#                                     kwargs={
#                                         'token': token
#                                     })
#                             )
#
#         except stripe.CardError as e:
#             message.info(request, "Your card has been declined.")
#
#     context = {
#         'order': existing_order,
#         'STRIPE_PUBLISHABLE_KEY': publishKey
#     }
#
#     return render(request, 'checkout2.html', context)
#
#
# def update_transaction_records(request, token):
#     # get the order being processed
#     order_to_purchase = get_user_pending_order(request)
#
#     # update the placed order
#     order_to_purchase.is_ordered = True
#     order_to_purchase.date_ordered = datetime.datetime.now()
#     order_to_purchase.save()
#
#     # get all items in the order - generates a queryset
#     order_items = order_to_purchase.items.all()
#
#     # update order items
#     order_items.update(is_ordered=True, date_ordered=datetime.datetime.now())
#
#     # Add products to user profile
#     user_profile = 'larce'
#     # get the products from the items
#     order_products = [item.product for item in order_items]
#     user_profile.ebooks.add(*order_products)
#     user_profile.save()
#
#     # create a transaction
#     transaction = Transaction(profile='0001',
#                               token=token,
#                               order_id=order_to_purchase.id,
#                               amount=order_to_purchase.get_cart_total(),
#                               success=True)
#     # save the transcation (otherwise doesn't exist)
#     transaction.save()
#
#     # send an email to the customer
#     # look at tutorial on how to send emails with sendgrid
#     messages.info(request, "Thank you! Your purchase was successful!")
#     return redirect(reverse('accounts:my_profile'))
#
