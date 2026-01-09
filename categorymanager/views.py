from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from categorymanager.models import Category
from categorymanager.serializers import CategorySerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def show_all_categories(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # POST
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def show_category_details(request, id):
    category = get_object_or_404(Category, pk=id)

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    if request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # PUT
    serializer = CategorySerializer(instance=category, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ensure_csrf_cookie
def categorymanager_ui(request):
    categories = Category.objects.all()
    return render(request, "categorymanager/categorymanager.html", {"categories": categories})
