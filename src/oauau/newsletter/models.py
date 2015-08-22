import uuid

from django.db import models


class Subscriber(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True,
                            default=uuid.uuid4)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.first_name or self.email.split('@')[0]


class List(models.Model):
    list_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return "%s (%s)" % (self.name, self.list_id)


class Subscription(models.Model):
    list = models.ForeignKey(List)
    subscriber = models.ForeignKey(Subscriber)

    def __str__(self):
        return "%s (%s)" % (self.subscriber, self.list)
