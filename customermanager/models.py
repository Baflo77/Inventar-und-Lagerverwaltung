from django.db import models
from django.conf import settings


class Customer(models.Model):
    salutation = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=100)

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"Name: {self.first_name} {self.last_name}, "
            f"E-Mail: {self.email}, "
            f"Telefon: {self.phone}"
        )
