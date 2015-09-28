from django.contrib import admin
from .models import Subscription, Subscriber, List


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'list_name', 'list_ident', 'joined',
                    'provider')
    list_filter = ('list__name', 'list__provider')
    search_fields = ('subscriber__first_name', 'subscriber__last_name',
                     'subscriber__email')

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
    list_display = ('first_name', 'last_name', 'email', 'registered')
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_id', 'provider')
    list_filter = ('provider',)
    search_fields = ('name', 'list_id')
