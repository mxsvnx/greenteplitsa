from django.contrib.auth.mixins import UserPassesTestMixin


class ChiefAgronomistRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        return user.is_superuser or user.groups.filter(name="chief_agronomist").exists()
