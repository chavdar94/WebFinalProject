from django.contrib.auth.mixins import UserPassesTestMixin, AccessMixin
from django.http import Http404


class GroupRequiredMixin(AccessMixin):
    allowed_groups = []

    def dispatch(self, request, *args, **kwargs):
        user_groups = request.user.groups.values_list('name', flat=True)
        if not set(self.allowed_groups) or not set(user_groups):
            raise Http404()
        return super().dispatch(request, *args, **kwargs)
