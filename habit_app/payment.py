from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import UserProfile
from .utils import get_current_utc

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def purchase_streak(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    stake_amount = max(1, int(request.POST.get('amount', 1)))
    stake_amount_cents = stake_amount * 100

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Stake an amount',
                    },
                    'unit_amount': stake_amount_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://habitstake.com/profile/',
            cancel_url='https://habitstake.com/profile/',
            metadata={'user_id': str(user_profile)}
        )
    except Exception as e:
        return HttpResponse(e)

    return redirect(checkout_session.url, status=303)

@csrf_exempt
def stripe_webhook(request):
    print("HELLO THERE")

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Successful Payment
    if event['type'] == 'checkout.session.completed':
        payment_intent = event['data']['object']
        user_id = payment_intent['metadata']['user_id']
        restart_streak(user_id)

    return HttpResponse(status=200)

def restart_streak(user_id):
    user_profile = get_object_or_404(UserProfile, user__username=user_id)
    utc_time_str = get_current_utc()
    user_profile.checkins.append(utc_time_str)
    user_profile.save()
