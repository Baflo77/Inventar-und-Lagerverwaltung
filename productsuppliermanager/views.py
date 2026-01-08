from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import ProductSupplier
from .serializers import ProductSupplierSerializer
from django.shortcuts import render
from productmanager.models import Product
from suppliermanager.models import Supplier
from .models import ProductSupplier

# Create your views here.
class ProductSupplierViewSet(viewsets.ModelViewSet):
    queryset = ProductSupplier.objects.all()
    serializer_class = ProductSupplierSerializer

def productsupplier_list_ui(request):
    # alle Zuordnungen anzeigen
    links = ProductSupplier.objects.select_related("product", "supplier").all().order_by("id")
    products = Product.objects.all().order_by("name")
    suppliers = Supplier.objects.all().order_by("name")
    return render(request, "productsuppliermanager/productsuppliermanager.html", {
        "links": links,
        "products": products,
        "suppliers": suppliers,
    })
