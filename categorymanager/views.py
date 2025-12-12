from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404

from categorymanager.models import Category


# Create your views here.
def show_categories(request):
    return HttpResponse("Hier sind deine Kategorien")

def show_all_categories_by_id(request, id):
    category = get_list_or_404(Category, id__gte=id)
    return_value =""
    for ca in category:
        return_value += f"{ca} "
    return HttpResponse(category)

def show_category_details(request, id):
    category = get_object_or_404(Category, pk=id)
    return HttpResponse(category)

def show_first_category(request):
    category = Category.objects.first()
    return HttpResponse(f"Name: {category.name}")

def write_category(request):
    category = Category(name="Elektronik")
    category.save()
    category = Category.objects.last()
    return HttpResponse(f"Name: {category.name}")
