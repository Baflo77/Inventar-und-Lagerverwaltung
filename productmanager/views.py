from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def show_products(request):
    return HttpResponse("Hier sind deine Produkte")


def show_product_details(request, id):
    return HttpResponse(f"Hier sind deine Details zu dem Produkt mit der ID {id}")