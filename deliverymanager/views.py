from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import Delivery
from .serializers import DeliverySerializer


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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


def deliveries_page(request):
    return render(request, "deliverymanager/deliveries.html")

def delivery_create(request):
    return render(request, "deliverymanager/delivery_create.html")


# Create your views here.
