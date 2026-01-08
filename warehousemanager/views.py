from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view
from yaml import serialize
from django.db.models import Count, Sum
from .models import Warehouse
from rest_framework.response import Response
from warehousemanager.serializers import WarehouseSerializer

# Create your views here.
def show_warehouses(request):
    return HttpResponse("Hier sind deine Warenhäuser")

@api_view()
def show_all_warehouses_by_id(request, id):
    warehouse = get_list_or_404(Warehouse, pk=id)
    serializer = WarehouseSerializer(warehouse)
    return Response(serializer.data)

def show_first_warehouse(request):
    warehouse = Warehouse.objects.first()
    return HttpResponse(f"Name: {warehouse.name}, Standort: {warehouse.location}")

def write_warehouse(request):
    warehouse = Warehouse(name="Warenhaus Technik", location="Würzburg")
    warehouse.save()
    warehouse = Warehouse.objects.last()
    return HttpResponse(f"Name: {warehouse.name}, Standort: {warehouse.location}")


def show_warehouses_ui(request):

    warehouses = Warehouse.objects.annotate(location_count=Count('locations', distinct=True),total_stock_quantity=Sum('locations__stock_items__quantity')
    )

    context = {'warehouses': warehouses}
    return render(request, 'warehousemanager/warehousemanager.html', context)