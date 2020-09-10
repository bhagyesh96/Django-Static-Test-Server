from django import forms

#from webpush.models import Group, PushInformation, SubscriptionInfo
from .models import PushInformationData,SubscriptionData


class WebPushForm(forms.Form):
    group = forms.CharField(max_length=255, required=False)
    status_type = forms.ChoiceField(choices=[
                                      ('subscribe', 'subscribe'),
                                      ('unsubscribe', 'unsubscribe')
                                    ])

    def save_or_delete(self, subscription, user, status_type, group_name):
        data = {}

        if user.is_authenticated:
            data["user"] = user

        if group_name:
            group, created = Group.objects.get_or_create(name=group_name)
            data["group"] = group

        data["subscription"] = subscription

        push_info, created = PushInformationData.objects.get_or_create(**data)

        # If unsubscribe is called, that means need to delete the browser
        # and notification info from server. 
        if status_type == "unsubscribe":
            push_info.delete()
            subscription.delete()


class SubscriptionForm(forms.ModelForm):

    class Meta:
        model = SubscriptionData
        fields = ('endpoint', 'auth', 'p256dh', 'browser')

    def get_or_save(self):
        subscription, created = SubscriptionData.objects.get_or_create(**self.cleaned_data)
        return subscription



class WebPushDataForm(forms.Form):
    status_type = forms.ChoiceField(choices=[
                                      ('subscribe', 'subscribe'),
                                      ('unsubscribe', 'unsubscribe')
                                    ])

    def save_or_delete(self, subscription, status_type):
        data = {}

        data["subscription"] = subscription

        push_info, created = PushInformationData.objects.get_or_create(**data)

        # If unsubscribe is called, that means need to delete the browser
        # and notification info from server. 
        if status_type == "unsubscribe":
            push_info.delete()
            subscription.delete()

class SubscriptionDataForm(forms.ModelForm):

    class Meta:
        model = SubscriptionData
        fields = ('endpoint', 'auth', 'p256dh', 'browser')

    def get_or_save(self):
        subscription, created = SubscriptionData.objects.get_or_create(**self.cleaned_data)
        return subscription