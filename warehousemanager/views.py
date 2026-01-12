from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models.functions import Coalesce
from django.db.models import Count, Sum

from stockmanager.models import Stock
from .models import Warehouse
from .serializers import WarehouseSerializer

@permission_classes([IsAuthenticated])
def warehouse_list_ui(request):
    min_locations = request.GET.get("min_locations")
    min_capacity = request.GET.get("min_capacity")
    max_capacity = request.GET.get("max_capacity")
    sort = request.GET.get("sort")
    direction = request.GET.get("dir")

    warehouses = Warehouse.objects.annotate(
        location_count=Count("locations", distinct=True),
        total_stock_quantity=Coalesce(Sum("locations__stocks__quantity"), 0),
        total_capacity=Coalesce(Sum("locations__capacity"), 0),
    )

    try:
        if min_locations not in (None, ""):
            warehouses = warehouses.filter(location_count__gte=int(min_locations))
        if min_capacity not in (None, ""):
            warehouses = warehouses.filter(total_capacity__gte=int(min_capacity))
        if max_capacity not in (None, ""):
            warehouses = warehouses.filter(total_capacity__lte=int(max_capacity))
    except ValueError:
        pass

    if sort == "capacity":
        order = "total_capacity" if direction == "asc" else "-total_capacity"
        warehouses = warehouses.order_by(order)
    else:
        warehouses = warehouses.order_by("name")

    return render(request, "warehousemanager/warehousemanager.html", {
        "warehouses": warehouses,
        "min_locations": min_locations or "",
        "min_capacity": min_capacity or "",
        "max_capacity": max_capacity or "",
        "sort": sort or "",
        "dir": direction or "",
    })



@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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

def warehouse_delete_ui(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)

    total_qty = (
        Stock.objects
        .filter(location__warehouse=warehouse)
        .aggregate(total=Sum("quantity"))
        .get("total") or 0
    )

    if request.method != "POST":
        return redirect("warehouse_list_ui")

    if total_qty > 0:
        messages.warning(
            request,
            f"Warehouse „{warehouse.name}“ kann nicht gelöscht werden, weil noch {total_qty} Stück eingelagert sind. "
            "Bitte Produkte umlagern, damit das Lager leer ist."
        )
        return redirect("warehouse_list_ui")

    if warehouse.locations.exists():
        messages.warning(
            request,
            f"Warehouse „{warehouse.name}“ kann nicht gelöscht werden, weil noch Standorte (Locations) existieren. "
            "Bitte zuerst Standorte entfernen oder umhängen."
        )
        return redirect("warehouse_list_ui")

    warehouse.delete()
    messages.success(request, "Warehouse wurde gelöscht.")
    return redirect("warehouse_list_ui")