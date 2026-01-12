from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.exceptions import PermissionDenied


# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def showallorders(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializedorders = OrderSerializer(orders, many=True)
        return Response(serializedorders.data)
    elif request.method == 'POST':
        orderserializer = OrderSerializer(data=request.data)
        if orderserializer.is_valid():
            orderserializer.save()
            return Response(orderserializer.data, status=status.HTTP_201_CREATED)
        return Response(orderserializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def show_order_details(request, id):
    order = get_object_or_404(Order, pk=id)
    if request.method == "GET":
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    elif request.method == "DELETE":
        order.delete()
        return Response(data="msg: Die Order wurde gelöscht", status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        order_serializer = OrderSerializer(instance=order, data=request.data)
        if order_serializer.is_valid():
            order_serializer.save()
            return Response(order_serializer.data)
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def showallorderitems(request):
    if request.method == 'GET':
        orderitems = OrderItem.objects.all()
        serializeditems = OrderItemSerializer(orderitems, many=True)
        return Response(serializeditems.data)
    elif request.method == 'POST':
        itemserializer = OrderItemSerializer(data=request.data)
        if itemserializer.is_valid():
            itemserializer.save()
            return Response(itemserializer.data, status=status.HTTP_201_CREATED)
        return Response(itemserializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def show_order_item_details(request, id):
    order_item = get_object_or_404(OrderItem, pk=id)
    if request.method == "GET":
        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data)
    elif request.method == "DELETE":
        order_item.delete()
        return Response(data="msg: Das OrderItem wurde gelöscht", status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        item_serializer = OrderItemSerializer(instance=order_item, data=request.data)
        if item_serializer.is_valid():
            item_serializer.save()
            return Response(item_serializer.data)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None

def ordermanager_ui(request):
    orders = Order.objects.all()
    return render(request, "ordermanager/ordermanager.html", {"orders": orders})