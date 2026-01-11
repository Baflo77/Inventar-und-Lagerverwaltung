from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from .models import ProductSupplier
from .serializers import ProductSupplierSerializer
from productmanager.models import Product
from suppliermanager.models import Supplier
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q

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
    qty_raw = request.query_params.get("quantity")
    qs = ProductSupplier.objects.select_related("product", "supplier").all().order_by("id")

    if product_id:
        qs = qs.filter(product_id=product_id)

    if qty_raw: #Menge filtern für purchaseorder
        try:
            qty = int(qty_raw)
            if qty > 0:
                qs = qs.filter(Q(min_order_quantity__lte=qty) | Q(min_order_quantity__isnull=True))
        except (ValueError, TypeError):
            pass

    return Response(ProductSupplierSerializer(qs, many=True).data)

@api_view(["GET"])
@permission_classes([AllowAny])
def productsupplier_by_supplier(request):
    supplier_id = request.query_params.get("supplier_id")

    qs = ProductSupplier.objects.select_related(
        "product",
        "supplier"
    ).all().order_by("id")

    if supplier_id:
        qs = qs.filter(supplier_id=supplier_id)

    return Response(ProductSupplierSerializer(qs, many=True).data)