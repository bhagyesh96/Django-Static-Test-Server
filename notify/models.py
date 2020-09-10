from django.db import models

class SubscriptionData(models.Model):
    browser = models.CharField(max_length=100)
    endpoint = models.URLField(max_length=500)
    auth = models.CharField(max_length=100)
    p256dh = models.CharField(max_length=100)


class PushInformationData(models.Model):

    subscription = models.ForeignKey(SubscriptionData, related_name='webpushdata_info', on_delete=models.CASCADE)
    #group = models.ForeignKey(Group, related_name='webpushdata_info', blank=True, null=True, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Check whether user or the group field is present
        # At least one field should be present there
        # Through from the functionality its not possible, just in case! ;)
        #if self.user or self.group:
        super(PushInformationData, self).save(*args, **kwargs)
        #else:
            #raise FieldError('At least user or group should be present')
