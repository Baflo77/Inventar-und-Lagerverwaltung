from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def show_categories(request):
    return HttpResponse("Hier sind deine Kategorien")


def show_category_details(request, id):
    return HttpResponse(f"Hier sind deine Details zu der Kategorie mit der ID {id}")