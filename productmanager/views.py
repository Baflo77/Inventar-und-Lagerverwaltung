from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from productmanager.models import Product
from productmanager.serializers import ProductSerializer
from suppliermanager.models import Supplier
from categorymanager.models import Category


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def show_all_products(request):
    if request.method == "GET":
        searchterm = request.query_params.get("searchterm")
        if searchterm:
            products = Product.objects.filter(name__icontains=searchterm)
        else:
            products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def show_product_details(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = ProductSerializer(instance=product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ensure_csrf_cookie
def product_list_ui(request):
    searchterm = request.GET.get("searchterm")
    if searchterm:
        products = Product.objects.filter(name__icontains=searchterm)
    else:
        products = Product.objects.all()

    suppliers = Supplier.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        "productmanager/productmanager.html",
        {
            "products": products,
            "suppliers": suppliers,
            "categories": categories,
        },
    )
