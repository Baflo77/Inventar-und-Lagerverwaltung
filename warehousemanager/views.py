from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Warehouse
from .serializers import WarehouseSerializer


def warehouse_list_ui(request):
    # location_count kommt aus Location.related_name="locations"
    warehouses = Warehouse.objects.annotate(location_count=Count("locations"))
    return render(request, "warehousemanager/warehousemanager.html", {"warehouses": warehouses})


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def show_all_warehouses(request):
    if request.method == "GET":
        warehouses = Warehouse.objects.all()
        return Response(WarehouseSerializer(warehouses, many=True).data)

    wh_serializer = WarehouseSerializer(data=request.data)
    if wh_serializer.is_valid():
        wh_serializer.save()
        return Response(wh_serializer.data, status=status.HTTP_201_CREATED)
    return Response(wh_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def show_warehouse_detail(request, id):
    warehouse = get_object_or_404(Warehouse, pk=id)

    if request.method == "GET":
        return Response(WarehouseSerializer(warehouse).data)

    if request.method == "PUT":
        wh_serializer = WarehouseSerializer(warehouse, data=request.data)
        if wh_serializer.is_valid():
            wh_serializer.save()
            return Response(wh_serializer.data)
        return Response(wh_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        warehouse.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)