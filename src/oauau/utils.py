from django.views.generic import ListView, View, FormView
from django.template import RequestContext
from django.template.loader import get_template
from django import http


class JsonView(View):
    """ By using this class, the methods json_get and json_post needs to be
    implemented.
    """

    def get(self, request, *args, **kwargs):
        try:
            data = self.json_get(request)
            return http.JsonResponse({'success': True, 'data': data})
        except Exception as err:
            return http.JsonResponse({'success': False, 'message': str(err)})

    def post(self, request, *args, **kwargs):
        try:
            data = self.json_post(request)
            return http.JsonResponse({'success': True, 'data': data})
        except Exception as err:
            return http.JsonResponse({'success': False, 'message': str(err)})

    def json_get(self, request, *args, **kwargs):
        raise NotImplementedError

    def json_post(self, request, *args, **kwargs):
        raise NotImplementedError


class JsonFormView(FormView):

    success_url = '/'
    form_template = None

    def form_valid(self, form):
        return http.JsonResponse({'success': True,
                                  'success_url': self.success_url})

    def form_invalid(self, form, extra_data=None):
        template = get_template(self.form_template)
        context = RequestContext(self.request, {'form': form})
        html = template.render(context)
        data = {'success': False, 'html': html}
        if extra_data:
            data.update(extra_data)
        return http.JsonResponse(data)
