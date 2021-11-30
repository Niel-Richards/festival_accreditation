from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.
class User(AbstractUser):
    is_manager = models.BooleanField(default=False)    

    def get_absolute_url(self):
        return reverse('account:user_detail', kwargs={'id': self.id})

    def get_event(self, _slug):
       return self.authorised_for_event.filter(slug = _slug).exists()