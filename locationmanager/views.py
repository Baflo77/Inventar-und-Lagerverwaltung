from typing import Any

from django.shortcuts import render
from django.http import HttpResponse, request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Location
from rest_framework.response import Response

from .serializers import LocationSerializer


# Create your views here.
def show_locations(request):
    return HttpResponse("Hier sind die verschiedenen Standorte")

@api_view(["GET", "POST"])
def show_all_locations(request):
    if request.method == "GET":
        searchterm = request.query.get("searchterm")
        if searchterm is not None:
            location = Location.objects.filter(name__icontains=searchterm)
        elif searchterm is None:
            location = Location.objects.all()

        serialized_location = LocationSerializer(location, many=True)
        return Response(serialized_location.data)

    elif request.method == "POST":
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(LocationSerializer.data, status=status.HTTP_201_CREATED)
    return Response(LocationSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


def write_location(request):
    location = Location(address="Kurfürstendamm 1", warehouse="W3")
    location.save()
    location = Location.objects.last()
    return HttpResponse(f"Addresse: {location.address}, Warenhaus: {location.warehouse}")

