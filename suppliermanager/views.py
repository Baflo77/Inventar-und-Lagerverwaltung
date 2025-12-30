from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.permissions import IsAdminUser

from suppliermanager.models import Supplier
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from suppliermanager.serializers import SupplierSerializer


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def show_all_suppliers(request):
    if request.method == "GET":
        suppliers = get_list_or_404(Supplier)
        serialized_suppliers = SupplierSerializer(suppliers, many=True)
        return Response(serialized_suppliers.data)
    elif request.method == "POST":
        supplier_serializer = SupplierSerializer(data=request.data)
        if supplier_serializer.is_valid():
            supplier_serializer.save()
            return Response(supplier_serializer.data, status=status.HTTP_201_CREATED)
        return Response(supplier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
def show_supplier_details(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    if request.method == "GET":
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)
    elif request.method == "DELETE":
        supplier.delete()
        return Response(data="msg: Der Lieferant wurde gelöscht", status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        supplier_serializer = SupplierSerializer(instance=supplier, data=request.data)
        if supplier_serializer.is_valid():
            supplier_serializer.save()
            return Response(supplier_serializer.data)
        return Response(supplier_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None
