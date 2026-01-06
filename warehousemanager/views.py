from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from yaml import serialize

from .models import Warehouse
from rest_framework.response import Response
from warehousemanager.serializers import WarehouseSerializer

# Create your views here.
def show_warehouses(request):
    return HttpResponse("Hier sind deine Warenhäuser")

@api_view(["GET","POST"])
def show_all_warehouses(request):
    if request.method == "GET":
        searchterm = request.query.get("searchterm")
        if searchterm is not None:
            warehouses = Warehouse.objects.filter(name__icontains=searchterm)
        elif searchterm is None:
            warehouses = Warehouse.objects.all()

        serializer = WarehouseSerializer(warehouses)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = WarehouseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(WarehouseSerializer.data, status=status.HTTP_201_CREATED)
    return Response(WarehouseSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

def show_first_warehouse(request):
    warehouse = Warehouse.objects.first()
    return HttpResponse(f"Name: {warehouse.name}, Standort: {warehouse.location}")

def write_warehouse(request):
    warehouse = Warehouse(name="Warenhaus Technik", location="Würzburg")
    warehouse.save()
    warehouse = Warehouse.objects.last()
    return HttpResponse(f"Name: {warehouse.name}, Standort: {warehouse.location}")

def warehouse_list_ui(request):
    searchterm = request.GET.get("searchterm")
    if searchterm:
        warehouses = Warehouse.objects.filter(name__icontains=searchterm)
    else:
        warehouses = Warehouse.objects.all()

    return render(request, "warehousemanager/warehousemanager.html", {"warehouses": warehouses})