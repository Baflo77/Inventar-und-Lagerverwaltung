from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=30)
    contact_person = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=25)
    street = models.CharField(max_length=25)
    house_number = models.IntegerField()

    def __str__(self):
        return f"Name: {self.name}, Kontaktperson: {self.contact_person}, E-Mail: {self.email}, Telefon: {self.phone}, PLZ: {self.postal_code}, Stadt: {self.city}, Straße: {self.street}, Hausnummer: {self.house_number}"