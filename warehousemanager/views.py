from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Warehouse

# Create your views here.
def show_warehouses(request):
    return HttpResponse("Hier sind deine Warenhäuser")

def show_all_warehouses_by_id(request, id):
    warehouse = get_list_or_404(Warehouse, pk=id)
    return HttpResponse(warehouse)

def show_first_warehouse(request):
    warehouse = Warehouse.objects.first()
    return HttpResponse(f"Name: {warehouse.name}, Standort: {warehouse.location}")

def write_warehouse(request):
    warehouse = Warehouse(name="Warenhaus Technik", location="Würzburg")
    warehouse.save()
    warehouse = Warehouse.objects.last()
    return HttpResponse(f"Name: {warehouse.name}, Standort: {warehouse.location}")