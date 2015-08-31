from mailchimp import Mailchimp, ListAlreadySubscribedError
from madmimi import MadMimi

from django.conf import settings


class AlreadyRegisteredError(Exception):

    def __init__(self, message, uuid, *args, **kwargs):
        super(Exception, self).__init__(message, *args, **kwargs)
        self.uuid = uuid


class AlreadySubscribedError(AlreadyRegisteredError):
    pass


class EmailMarketing(object):

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if self.is_madmimi():
                self._client = MadMimi(settings.MADMIMI_USER,
                                       settings.MADMIMI_API_KEY)
            elif self.is_mailchimp():
                self._client = Mailchimp(settings.MAILCHIMP_API_KEY)
            else:
                raise NotImplementedError('EmailMarketing provider %s is '
                        'invalid.' % settings.CURRENT_EMAIL_MARKETING_PROVIDER)
        return self._client

    def is_madmimi(self):
        cur = settings.CURRENT_EMAIL_MARKETING_PROVIDER
        return cur == settings.MADMIMI

    def is_mailchimp(self):
        cur = settings.CURRENT_EMAIL_MARKETING_PROVIDER
        return cur == settings.MAILCHIMP

    def newsletter_id_name(self):
        if self.is_mailchimp():
            return settings.MAILCHIMP_NEWSLETTER_LIST_ID, \
                   settings.MAILCHIMP_NEWSLETTER_LIST_NAME
        elif self.is_madmimi():
            return settings.MADMIMI_NEWSLETTER_LIST_ID, \
                   settings.MADMIMI_NEWSLETTER_LIST_NAME
        else:
            raise NotImplementedError('EmailMarketing provider %s is '
                        'invalid.' % settings.CURRENT_EMAIL_MARKETING_PROVIDER)

    def oauau_id_name(self):
        if self.is_mailchimp():
            return settings.MAILCHIMP_OAUAU_LIST_ID, \
                   settings.MAILCHIMP_OAUAU_LIST_NAME
        elif self.is_madmimi():
            return settings.MADMIMI_OAUAU_LIST_ID, \
                   settings.MADMIMI_OAUAU_LIST_NAME
        else:
            raise NotImplementedError('EmailMarketing provider %s is '
                        'invalid.' % settings.CURRENT_EMAIL_MARKETING_PROVIDER)

    def subscribe_to_newsletter(self, email, **kwargs):
        list_id = self.newsletter_id_name()[0]
        self.subscribe(email, list_id, **kwargs)

    def unsubscribe_to_newsletter(self, email):
        list_id = self.newsletter_id_name()[0]
        self.unsubscribe(email, list_id)

    def subscribe_to_oauau(self, email, **kwargs):
        list_id = self.oauau_id_name()[0]
        self.subscribe(email, list_id, **kwargs)

    def unsubscribe_to_oauau(self, email):
        list_id = self.oauau_id_name()[0]
        self.unsubscribe(email, list_id)

    def subscribe(self, email, list_id, **kwargs):
        if self.is_mailchimp():
            try:
                self.client.lists.subscribe(list_id, dict(email=email), kwargs,
                                            double_optin=False)
            except ListAlreadySubscribedError as err:
                pass
                #raise AlreadySubscribedError(str(err))
        elif self.is_madmimi():
            contact = (kwargs.get('first_name'), kwargs.get('last_name'),
                       email, list_id)
            self.client.add_contacts([contact], audience_list=list_id)
            #self.client.subscribe(email, list_id)
        else:
            raise NotImplementedError('EmailMarketing provider %s is '
                        'invalid.' % settings.CURRENT_EMAIL_MARKETING_PROVIDER)

    def unsubscribe(self, email, list_id):
        if self.is_mailchimp():
            self.client.lists.unsubscribe(list_id, dict(email=email))
        elif self.is_madmimi():
            self.client.unsubscribe(email, list_id)
        else:
            raise NotImplementedError('EmailMarketing provider %s is '
                        'invalid.' % settings.CURRENT_EMAIL_MARKETING_PROVIDER)
