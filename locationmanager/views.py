from typing import Any

from django.shortcuts import render
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Location
from rest_framework.response import Response
from .serializers import LocationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count, Sum
from django.db.models.functions import Coalesce
from warehousemanager.models import Warehouse
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import Sum
from stockmanager.models import Stock

# Create your views here.
def location_list_ui(request):
    locations = (Location.objects.select_related('warehouse').annotate(item_count=Count('stocks'),total_quantity=Coalesce(Sum('stocks__quantity'), 0)).all()
    )

    warehouses = Warehouse.objects.all().order_by("name")

    context = {
        'locations': locations,
        'warehouses': warehouses,
    }
    return render(request, "locationmanager/locationmanager.html", context)


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def show_all_locations(request):
    if request.method == "GET":
        searchterm = request.query_params.get("searchterm")
        locations = Location.objects.all()

        if searchterm:
            locations = locations.filter(name__icontains=searchterm)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def location_detail(request, id):
    location = get_object_or_404(Location, pk=id)

    if request.method == "GET":
        return Response(LocationSerializer(location).data)

    if request.method == "PUT":
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def location_delete_ui(request, pk):
    location = get_object_or_404(Location, pk=pk)
    total_qty = location.stocks.aggregate(total=Sum("quantity")).get("total") or 0

    if request.method != "POST":
        return redirect("location_list_ui")

    if total_qty > 0:
        messages.warning(
            request,
            f"Standort „{location.name}“ kann nicht gelöscht werden, weil noch {total_qty} Stück dort lagern. "
            "Bitte umlagern."
        )
        return redirect("location_list_ui")

    location.delete()
    messages.success(request, "Standort wurde gelöscht.")
    return redirect("location_list_ui")