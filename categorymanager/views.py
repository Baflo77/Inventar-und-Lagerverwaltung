from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from categorymanager.models import Category
from categorymanager.serializers import CategorySerializer


# Create your views here.
@api_view(["GET", "POST"])
def show_all_categories(request):
    if request.method == "GET":
        categories = get_list_or_404(Category)
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data)
    elif request.method == "POST":
        category_serializer = CategorySerializer(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None

@api_view(["GET", "PUT", "DELETE"])
def show_category_details(request, id):
    category = get_object_or_404(Category, pk=id)
    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == "DELETE":
        category.delete()
        return Response(data="msg: Die Kategorie wurde gelöscht", status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        category_serializer = CategorySerializer(instance=category, data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None

