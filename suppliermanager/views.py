from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from suppliermanager.models import Supplier
from rest_framework.decorators import api_view
from rest_framework.response import Response
from suppliermanager.serializers import SupplierSerializer


# Create your views here.
@api_view(["GET", "POST"])
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


@api_view()
def show_all_suppliers_by_id(request, id):
    supplier = get_list_or_404(Supplier, id__gte=id)
    return_value =""
    for ca in supplier:
        return_value += f"{ca} "
    return Response(supplier)

@api_view(["GET", "PUT", "DELETE"])
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

def show_first_supplier(request):
    supplier = Supplier.objects.first()
    return HttpResponse(f"Name: {supplier.name}, Kontaktperson: {supplier.contact_person}, E-Mail: {supplier.email}, Telefon: {supplier.phone}, PLZ: {supplier.postal_code}, Stadt: {supplier.city}, Straße: {supplier.street}, Hausnummer: {supplier.house_number}")

def write_supplier(request):
    supplier = Supplier(name="Müller Elektrohandel", contact_person="Franz Müller", email="mail@mueller.de", phone="123456", postal_code="74228", city="Musterhausen", street="Musterstraße", house_number="12")
    supplier.save()
    supplier = Supplier.objects.last()
    return HttpResponse(f"Name: {supplier.name}, Kontaktperson: {supplier.contact_person}, E-Mail: {supplier.email}, Telefon: {supplier.phone}, PLZ: {supplier.postal_code}, Stadt: {supplier.city}, Straße: {supplier.street}, Hausnummer: {supplier.house_number}")