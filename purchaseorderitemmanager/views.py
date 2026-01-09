from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import PurchaseOrderItem
from .serializers import PurchaseOrderItemSerializer
from django.views.decorators.csrf import ensure_csrf_cookie


@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def purchaseorderitem_list(request):
    if request.method == "GET":
        po_id = request.query_params.get("purchase_order_id")

        items = PurchaseOrderItem.objects.all()

        if po_id:
            items = items.filter(purchase_order_id=po_id)

        return Response(PurchaseOrderItemSerializer(items, many=True).data)

    serializer = PurchaseOrderItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def purchaseorderitem_detail(request, id):
    item = get_object_or_404(PurchaseOrderItem, id=id)

    if request.method == "GET":
        return Response(PurchaseOrderItemSerializer(item).data)

    if request.method == "PUT":
        serializer = PurchaseOrderItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@ensure_csrf_cookie
def purchaseorderitem_ui(request):
    items = PurchaseOrderItem.objects.select_related("purchase_order", "purchase_order__supplier")
    return render(request, "purchaseorderitemmanager/purchaseorderitemmanager.html", {"items": items})



