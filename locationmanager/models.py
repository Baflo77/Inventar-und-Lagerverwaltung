from django.db import models

# Create your models here.
class Location(models.Model):
    address = models.CharField(max_length=100)

    def __str__(self):
        return f"Addresse: {self.address}, Warenhaus: {self.warehouse}"

