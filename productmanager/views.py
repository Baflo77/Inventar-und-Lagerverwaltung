from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from productmanager.models import Product
from productmanager.serializers import ProductSerializer


# Create your views here.
@api_view(["GET", "POST"])
def show_all_products(request):
    if request.method == "GET":
        searchterm = request.query_params.get('searchterm')
        if searchterm is not None:
            products = get_list_or_404(Product, name__contains=searchterm)
        else:
            products = get_list_or_404(Product)
        serialized_customers = ProductSerializer(products, many=True)
        return Response(serialized_customers.data)
    elif request.method == "POST":
        product_serializer = ProductSerializer(data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None


def show_all_products_by_id(request, id):
    product = get_list_or_404(Product, id__gte=id)
    return_value =""
    for ca in product:
        return_value += f"{ca} "
    return HttpResponse(product)

@api_view(["GET", "PUT", "DELETE"])
def show_product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == "DELETE":
        product.delete()
        return Response(data="msg: Das Produkt wurde gelöscht", status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        product_serializer = ProductSerializer(instance=product, data=request.data)
        if product_serializer.is_valid():
            product_serializer.save()
            return Response(product_serializer.data)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None

def show_first_product(request):
    product = Product.objects.first()
    return HttpResponse(f"Name: {product.name} SKU: {product.sku} Description: {product.description}, Supplier: {product.supplier}, Category: {product.category}")

def write_product(request):
    product = Product(name="Apple iPhone 15", sku="1234567", description="Ein iPhone 15", supplier="1", category="1")
    product.save()
    product = Product.objects.last()
    return HttpResponse(f"Name: {product.name} SKU: {product.sku} Description: {product.description}, Supplier: {product.supplier}, Category: {product.category}")