from django.db import models
from suppliermanager.models import Supplier
from categorymanager.models import Category

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productscategory')
    suppliers = models.ManyToManyField(Supplier, through="productsuppliermanager.ProductSupplier", related_name="products")

    def __str__(self):
        return f"{self.name} ({self.sku})"