from django.db import models

# Create your models here.
class Warehouse(models.Model):
    name = models.CharField(max_length=200)

    #location = models.ForeignKey('Location', on_delete=models.CASCADE , related_name='locations')

    def __str__(self):
        return f"Name: {self.name}, Standort: {self.location}"