from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model

class IsManagerMixin(UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_manager

class IsAuthorisedMixin(UserPassesTestMixin):
    
    def test_func(self):
        if self.request.user.get_event(self.kwargs.get('slug')) or self.request.user.is_manager:
            return True
        else:
            return False