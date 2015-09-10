from django.contrib import admin
from .models import Subscription, Subscriber, List


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'list_name', 'list_ident', 'provider')

    def list_name(self, obj):
        return obj.list.name
    list_name.admin_order_field = 'list__name'

    def list_ident(self, obj):
        return obj.list.list_id
    list_ident.short_description = 'List id'
    list_ident.admin_order_field = 'list__id'

    def provider(self, obj):
        return obj.list.provider
    provider.admin_order_field = 'list__provider'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_id', 'provider')
