from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from suppliermanager.models import Supplier


# Create your views here.
def show_suppliers(request):
    return HttpResponse("Hier ist dein Kunde")

def show_all_suppliers_by_id(request, id):
    supplier = get_list_or_404(Supplier, id__gte=id)
    return_value =""
    for ca in supplier:
        return_value += f"{ca} "
    return HttpResponse(supplier)

def show_supplier_details(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    return HttpResponse(supplier)

def show_first_supplier(request):
    supplier = Supplier.objects.first()
    return HttpResponse(f"Name: {supplier.name}, Kontaktperson: {supplier.contact_person}, E-Mail: {supplier.email}, Telefon: {supplier.phone}, PLZ: {supplier.postal_code}, Stadt: {supplier.city}, Straße: {supplier.street}, Hausnummer: {supplier.house_number}")

def write_supplier(request):
    supplier = Supplier(name="Müller Elektrohandel", contact_person="Franz Müller", email="mail@mueller.de", phone="123456", postal_code="74228", city="Musterhausen", street="Musterstraße", house_number="12")
    supplier.save()
    supplier = Supplier.objects.last()
    return HttpResponse(f"Name: {supplier.name}, Kontaktperson: {supplier.contact_person}, E-Mail: {supplier.email}, Telefon: {supplier.phone}, PLZ: {supplier.postal_code}, Stadt: {supplier.city}, Straße: {supplier.street}, Hausnummer: {supplier.house_number}")