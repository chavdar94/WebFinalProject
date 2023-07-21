from django.http import Http404


class NoDjangoAdminForEndUserMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def _middleware(self, request, *args, **kwargs):
        if request.path.startswith("/admin/"):
            if not request.user.is_authenticated or not request.user.is_staff:
                raise Http404()
        return None  # Return None when not raising Http404

    def __call__(self, request, *args, **kwargs):
        response = self._middleware(request, *args, **kwargs)
        if response is None:
            response = self.get_response(request, *args, **kwargs)
        return response
