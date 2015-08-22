# -*- coding: <nome da codificação> -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from ..utils import JsonFormView
from .client import AlreadySubscribedError
from .forms import SubscriberForm
from .models import Subscriber


class NewsletterBaseView(JsonFormView):

    already_msg = "You are already subscribed to my newsletter."

    def form_valid(self, form):
        try:
            subscriber = form.pre_subscribe_locally()
            form.send_confirmation(subscriber)
        except AlreadySubscribedError as err:
            form.errors['__all__'] = self.already_msg
            return self.form_invalid(form, extra_data={'s': err.uuid})
        return super(NewsletterBaseView, self).form_valid(form)


class NewsletterConfirmationBaseView(TemplateView):
    template_name = 'confirmation.html'
    redirect_name = None
    subscription_form_class = None

    def dispatch(self, request, *args, **kwargs):
        subscriber_uuid = request.GET.get('s')
        if not subscriber_uuid:
            return HttpResponseRedirect(reverse(self.redirect_name))
        try:
            subscriber = Subscriber.objects.get(uuid=subscriber_uuid)
        except Subscriber.DoesNotExist:
            return HttpResponseRedirect(reverse(self.redirect_name))
        form = self.subscription_form_class()
        form.subscribe(subscriber)
        return super(NewsletterConfirmationBaseView, self).dispatch(request,
                                                               *args, **kwargs)


class LandPageView(NewsletterBaseView):
    template_name = 'landpage.html'
    form_template = 'landingpage_form.html'
    form_class = SubscriberForm
    success_url = '/'
    redirect_name = 'landpage'


class ConfirmationView(NewsletterConfirmationBaseView):
    template_name = 'confirmation.html'
    subscription_form_class = SubscriberForm


class WorkbookView(NewsletterBaseView):
    template_name = 'workbook/signup.html'
    form_template = 'workbook/signup_form.html'
    form_class = SubscriberForm
    success_url = '/'
    already_msg = "Você já está cadastrado(a)"


class WorkbookConfirmationView(NewsletterConfirmationBaseView):
    template_name = 'workbook/signup_confirmation.html'
    redirect_name = 'workbook'
    subscription_form_class = SubscriberForm
