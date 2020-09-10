from django.shortcuts import render
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
#from webpush import send_user_notification
import json
from .forms import WebPushForm, SubscriptionForm,WebPushDataForm,SubscriptionDataForm


def home(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('publicKey')
    user = request.user
    return render(request, 'home.html', {user: user, 'vapid_key': vapid_key})

@require_POST
@csrf_exempt
def save_info(request):
    # Parse the  json object from post data. return 400 if the json encoding is wrong
    try:
        post_data = json.loads(request.body.decode('utf-8'))
    except ValueError:
        return HttpResponse(status=400)

    # Process the subscription data to mach with the model
    subscription_data = process_subscription_data(post_data)
    subscription_form = SubscriptionDataForm(subscription_data)
    # pass the data through WebPushForm for validation purpose
    web_push_form = WebPushDataForm(post_data)

    # Check if subscriptioninfo and the web push info bot are valid
    if subscription_form.is_valid() and web_push_form.is_valid():
        # Get the cleaned data in order to get status_type and group_name
        web_push_data = web_push_form.cleaned_data
        status_type = web_push_data.pop("status_type")
        #group_name = web_push_data.pop("group")

        # We at least need the user or group to subscribe for a notification
        #if request.user.is_authenticated or group_name:
            # Save the subscription info with subscription data
            # as the subscription data is a dictionary and its valid
        subscription = subscription_form.get_or_save()
        web_push_form.save_or_delete(subscription=subscription, status_type=status_type)

            # If subscribe is made, means object is created. So return 201
        if status_type == 'subscribe':
            return HttpResponse(status=201)
            # Unsubscribe is made, means object is deleted. So return 202
        elif "unsubscribe":
            return HttpResponse(status=202)

    

def process_subscription_data(post_data):
    """Process the subscription data according to out model"""
    subscription_data = post_data.pop("subscription", {})
    # As our database saves the auth and p256dh key in separate field,
    # we need to refactor it and insert the auth and p256dh keys in the same dictionary
    keys = subscription_data.pop("keys", {})
    subscription_data.update(keys)
    # Insert the browser name
    subscription_data["browser"] = post_data.pop("browser")
    return subscription_data       

@require_POST
@csrf_exempt
def send_push(request):
    try:
        body = request.body
        data = json.loads(body)

        if 'head' not in data or 'body' not in data or 'id' not in data:
            return JsonResponse(status=400, data={"message": "Invalid data format"})

        user_id = data['id']
        user = get_object_or_404(User, pk=user_id)
        payload = {'head': data['head'], 'body': data['body']}
        send_user_notification(user=user, payload=payload, ttl=1000)

        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})