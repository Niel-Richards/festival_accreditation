from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Company {self.name}"