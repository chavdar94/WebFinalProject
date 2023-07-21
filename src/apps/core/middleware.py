from django.http import Http404


class NoDjangoAdminForEndUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def _middleware(self, request, *args, **kwargs):
        if request.path.startswith("/admin/"):
            if not request.user.is_authenticated or not request.user.is_staff:
                raise Http404()
        response = self.get_response(request)
        return response

    def __call__(self, request, *args, **kwargs):
        self._middleware(request, *args, **kwargs)
        return self.get_response(request, *args, **kwargs)
