# -*- coding: <nome da codificação> -*-

from django.conf import settings
from django import forms
from django.core.mail import send_mail

from .client import EmailMarketing, AlreadySubscribedError, \
                    AlreadyRegisteredError
from .models import Subscriber, List, Subscription


BASE_URL = 'http://www.oauau.com.br'


class BaseSubscriberForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=255, required=False)
    last_name = forms.CharField(max_length=255, required=False)

    confirmation_url = '%s/confirmation/?s=%%s' % BASE_URL
    list_id = None
    name = None
    subject = ""
    body = ""

    def pre_subscribe_locally(self):
        data = self.cleaned_data
        try:
            subscriber = Subscriber.objects.get(email=data['email'])
            if subscriber.subscription_set\
                         .filter(list__list_id=self.list_id).count():
                raise AlreadySubscribedError('User %s is already subscribed.'
                                             % data['email'], subscriber.uuid)
            elif subscriber.subscription_set.all().count():
                raise AlreadyRegisteredError('User %s is already registered.'
                                             % data['email'], subscriber.uuid)
        except Subscriber.DoesNotExist:
            subscriber = Subscriber.objects.get_or_create(**data)[0]
        return subscriber

    def send_confirmation(self, subscriber):
        email = self.cleaned_data['email']
        redirect = self.confirmation_url % subscriber.uuid
        body = self.body % (str(subscriber), redirect)
        send_mail(self.subject, body, settings.DEFAULT_FROM_EMAIL, [email])

    def subscribe(self, subscriber):
        email = subscriber.email
        client = EmailMarketing()
        #try:
        #    client.unsubscribe(email, self.list_id)
        #except:
        #    pass
        #if settings.DEVELOPMENT:
        #    return
        client.subscribe(email, self.list_id, first_name=subscriber.first_name,
                        last_name=subscriber.last_name)
        list_id, list_name = self.list_id, self.name
        slist = List.objects.get_or_create(list_id=list_id, name=list_name,
                         provider=settings.CURRENT_EMAIL_MARKETING_PROVIDER)[0]
        Subscription.objects.get_or_create(list=slist, subscriber=subscriber)

    def is_subscribed(self, subscriber):
        return Subscription.objects.filter(list__list_id=self.list_id,
                                           subscriber=subscriber).exists()


class WorkbookSubscriberForm(BaseSubscriberForm):

    subject = "Confirme seu email"
    body = "Olá %s, \n\n" \
        "Clique no link abaixo para fazer o download do livro de atividades " \
        "do au au.\n\n" \
        "%s\n\n" \
        "Caso o link acima esteja inativo, copie e cole no seu browser.\n\n" \
        "Obrigada,\n\n" \
        "Flavia Bernardes e o au au"

    confirmation_url = '%s/livro-de-atividades-vogais/download/?s=%%s' % \
                       BASE_URL

    list_id = settings.MAILCHIMP_WORKBOOK_LIST_ID
    name = settings.MAILCHIMP_WORKBOOK_LIST_NAME


class LaunchSubscriberForm(BaseSubscriberForm):

    subject = "Confirme seu email"
    body = "Olá %s, \n\n" \
        "Confirme seu email clicando no link abaixo para ser o primeiro a " \
        "saber quando o livro do au au for lançado.\n\n" \
        "%s\n\n"\
        "Caso o link acima esteja inativo, copie e cole no seu browser.\n\n" \
        "Obrigada,\n\n" \
        "Flavia Bernardes e o au au"

    confirmation_url = '%s/confirmacao/?s=%%s' % BASE_URL

    list_id = settings.MAILCHIMP_LAUNCH_LIST_ID
    name = settings.MAILCHIMP_LAUNCH_LIST_NAME
