from django.db import models
from django.conf import settings
# Create your models here.
class Customer(models.Model):
    salutation = models.CharField(max_length=100)
    '''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    '''
    phone = models.CharField(max_length=100)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
         return f"Order {self.id} ({self.customer})"

    def first_name(self):
        return self.first_name

    def last_name(self):
        return self.last_name

    def email(self):
        return self.email
