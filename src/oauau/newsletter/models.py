import uuid

from django.db import models


class Subscriber(models.Model):
    uuid = models.CharField(max_length=100, blank=True, unique=True,
                            default=uuid.uuid4)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    registered = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.full_name or self.email.split('@')[0]

    @property
    def full_name(self):
        return ("%s %s" % (self.first_name, self.last_name)).strip()


class List(models.Model):
    provider = models.CharField(max_length=32)
    list_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128)

    class Meta:
        unique_together = (('provider', 'list_id', 'name'),)

    def __str__(self):
        return "%s (%s)" % (self.name, self.list_id)


class Subscription(models.Model):
    list = models.ForeignKey(List)
    subscriber = models.ForeignKey(Subscriber)
    joined = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = (('list', 'subscriber'),)

    def __str__(self):
        return "%s (%s)" % (self.subscriber, self.list)
