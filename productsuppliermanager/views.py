from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import ProductSupplier
from .serializers import ProductSupplierSerializer
from django.shortcuts import render
from productmanager.models import Product
from suppliermanager.models import Supplier
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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

@api_view(["GET"])
@permission_classes([AllowAny])
def productsupplier_by_product(request):
    product_id = request.query_params.get("product_id")

    qs = ProductSupplier.objects.select_related("product", "supplier").all().order_by("id")

    if product_id:
        qs = qs.filter(product_id=product_id)

    return Response(ProductSupplierSerializer(qs, many=True).data)

