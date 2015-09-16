# -*- coding: <nome da codificação> -*-

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import TemplateView

from ..utils import JsonFormView
from .client import AlreadyRegisteredError, AlreadySubscribedError
from .forms import WorkbookSubscriberForm, Promotion5DaysSubscriberForm
from .models import Subscriber


class NewsletterBaseView(JsonFormView):

    already_msg = "You are already subscribed to my newsletter."

    def form_valid(self, form, extra_data=None):
        try:
            subscriber = form.pre_subscribe_locally()
            form.send_confirmation(subscriber)
        except AlreadySubscribedError as err:
            extra_data = {'s': err.uuid, 'subs': True}
            return super(NewsletterBaseView, self).form_valid(form,
                                                         extra_data=extra_data)
        except AlreadyRegisteredError as err:
            extra_data = {'s': err.uuid}
            return super(NewsletterBaseView, self).form_valid(form,
                                                         extra_data=extra_data)
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
        if not request.GET.get("subs") or not form.is_subscribed(subscriber):
            form.subscribe(subscriber)
        return super(NewsletterConfirmationBaseView, self).dispatch(request,
                                                               *args, **kwargs)


class LandingPageView(NewsletterBaseView):
    template_name = 'landing_page.html'
    form_template = 'signup_form.html'
    form_class = Promotion5DaysSubscriberForm
    success_url = reverse_lazy("launch_confirmation")
    already_msg = "Você já está cadastrado(a)"


class LaunchConfirmationView(NewsletterConfirmationBaseView):
    template_name = 'promotion_5_days_confirmation.html'
    redirect_name = 'landing_page'
    subscription_form_class = Promotion5DaysSubscriberForm


class WorkbookView(NewsletterBaseView):
    template_name = 'workbook/signup.html'
    form_template = 'signup_form.html'
    form_class = WorkbookSubscriberForm
    success_url = reverse_lazy("workbook_confirmation")
    already_msg = "Você já está cadastrado(a)"


class WorkbookConfirmationView(NewsletterConfirmationBaseView):
    template_name = 'workbook/signup_confirmation.html'
    redirect_name = 'workbook'
    subscription_form_class = WorkbookSubscriberForm
