from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def show_suppliers(request):
    return HttpResponse("Hier ist dein Kunde")


def show_supplier_details(request, id):
    return HttpResponse(f"Hier sind deine Details zu dem Lieferanten mit der ID {id}")