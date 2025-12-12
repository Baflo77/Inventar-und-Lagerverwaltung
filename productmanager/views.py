from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from productmanager.models import Product


# Create your views here.
def show_products(request):
    return HttpResponse("Hier sind deine Produkte")

def show_all_products_by_id(request, id):
    product = get_list_or_404(Product, id__gte=id)
    return_value =""
    for ca in product:
        return_value += f"{ca} "
    return HttpResponse(product)

def show_product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    return HttpResponse(product)

def show_first_product(request):
    product = Product.objects.first()
    return HttpResponse(f"Name: {product.name} SKU: {product.sku} Description: {product.description}, Supplier: {product.supplier}, Category: {product.category}")

def write_product(request):
    product = Product(name="Apple iPhone 15", sku="1234567", description="Ein iPhone 15", supplier="1", category="1")
    product.save()
    product = Product.objects.last()
    return HttpResponse(f"Name: {product.name} SKU: {product.sku} Description: {product.description}, Supplier: {product.supplier}, Category: {product.category}")