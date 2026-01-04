from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework.decorators import api_view

from .models import Location
from rest_framework.response import Response

# Create your views here.
def show_locations(request):
    return HttpResponse("Hier sind die verschiedenen Standorte")

@api_view()
def show_all_locations_by_id(request, id):
    warehouse = get_list_or_404(Location, pk=id)
    return Response(warehouse)

def write_location(request):
    location = Location(address="Kurfürstendamm 1", warehouse="W3")
    location.save()
    location = Location.objects.last()
    return HttpResponse(f"Addresse: {location.address}, Warenhaus: {location.warehouse}")

