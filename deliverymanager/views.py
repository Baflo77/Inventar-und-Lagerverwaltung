from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Delivery
from .serializers import DeliverySerializer


@api_view(["GET", "POST"])
def show_deliveries(request):
    if request.method == "GET":
        deliveries = Delivery.objects.all()
        serializer = DeliverySerializer(deliveries, many=True)
        return Response(serializer.data)

    serializer = DeliverySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def show_delivery_details(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)

    if request.method == "GET":
        return Response(DeliverySerializer(delivery).data)

    if request.method == "PUT":
        serializer = DeliverySerializer(delivery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    delivery.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


from django.shortcuts import render

# Create your views here.
