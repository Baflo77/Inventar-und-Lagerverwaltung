from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from suppliermanager.models import Supplier
from suppliermanager.serializers import SupplierSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def show_all_suppliers(request):
    if request.method == "GET":
        suppliers = Supplier.objects.all()
        return Response(SupplierSerializer(suppliers, many=True).data)

    serializer = SupplierSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def show_supplier_details(request, id):
    supplier = get_object_or_404(Supplier, pk=id)

    if request.method == "GET":
        return Response(SupplierSerializer(supplier).data)

    if request.method == "DELETE":
        supplier.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = SupplierSerializer(instance=supplier, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ensure_csrf_cookie
def suppliermanager_ui(request):
    suppliers = Supplier.objects.all()
    return render(request, "suppliermanager/suppliermanager.html", {"suppliers": suppliers})
