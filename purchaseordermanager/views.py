from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def purchaseorder_list(request):
    if request.method == "GET":
        orders = PurchaseOrder.objects.all().order_by("-created_at")
        return Response(PurchaseOrderSerializer(orders, many=True).data)

    serializer = PurchaseOrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def purchaseorder_detail(request, id):
    order = get_object_or_404(PurchaseOrder, id=id)

    if request.method == "GET":
        return Response(PurchaseOrderSerializer(order).data)

    if request.method == "PUT":
        serializer = PurchaseOrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

def purchaseorder_ui(request):
    orders = PurchaseOrder.objects.all().order_by("-created_at")
    return render(request, "purchaseordermanager/purchaseordermanager.html/")
