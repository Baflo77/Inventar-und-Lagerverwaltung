from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404, render
from .models import PurchaseOrderItem
from .serializers import PurchaseOrderItemSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import transaction


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def purchaseorderitem_list(request):
    if request.method == "GET":
        po_id = request.query_params.get("purchase_order_id")
        items = PurchaseOrderItem.objects.select_related(
            "purchase_order",
            "product_supplier",
            "product_supplier__product",
            "product_supplier__supplier",
        )
        if po_id:
            items = items.filter(purchase_order_id=po_id)
        return Response(PurchaseOrderItemSerializer(items, many=True).data)

    payload = request.data
    is_bulk = isinstance(payload, list)


    if is_bulk:
        for idx, row in enumerate(payload, start=1):
            row.setdefault("line_no", idx)
    else:
        payload.setdefault("line_no", 1)

    serializer = PurchaseOrderItemSerializer(data=payload, many=is_bulk)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        serializer.save()

    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
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



