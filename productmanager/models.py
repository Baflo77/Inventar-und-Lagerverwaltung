from django.db import models
from suppliermanager.models import Supplier
from categorymanager.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    description = models.TextField()

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='products-supplier')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products-category')

    def __str__(self):
        return f"Name: {self.name}, SKU: {self.sku}, Beschreibung: {self.description}, Lieferant: {self.supplier}, Kategorie: {self.category}"