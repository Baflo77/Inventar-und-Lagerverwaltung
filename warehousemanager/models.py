from django.db import models

from locationmanager.models import Location as PhysicalLocation


class Warehouse(models.Model):
    location = models.OneToOneField(PhysicalLocation,on_delete=models.PROTECT,related_name='warehouse_data',verbose_name="Physischer Standort")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Warenhaus"
        verbose_name_plural = "Warenhäuser"

    def __str__(self):
        return f"{self.name}"

