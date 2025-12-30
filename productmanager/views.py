from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from productmanager.models import Product
from productmanager.serializers import ProductSerializer


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
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

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdminUser])
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

