from django.contrib.auth.mixins import UserPassesTestMixin


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = None

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return self.group_required in user_groups
