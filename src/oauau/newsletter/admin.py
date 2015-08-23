from django.contrib import admin
from .models import Subscription, Subscriber, List


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    pass


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    pass
