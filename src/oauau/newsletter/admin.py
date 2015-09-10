from django.contrib import admin
from .models import Subscription, Subscriber, List


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'list_name', 'list_ident', 'provider')

    def list_name(self, obj):
        return obj.list.name

    def list_ident(self, obj):
        return obj.list.list_id
    list_ident.short_description = 'List id'

    def provider(self, obj):
        return obj.list.provider


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_id', 'provider')
