from django.db import models
from django.conf import settings


class Customer(models.Model):
    salutation = models.CharField(max_length=100)

    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    '''
    phone = models.CharField(max_length=100)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        null=True,
        blank=True,
    )
    ''' # sorgt für RecursionError
    def __str__(self):
        return f"{self.first_name} {self.last_name} (Customer #{self.id})"
    '''

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def email(self):
        return self.user.email


