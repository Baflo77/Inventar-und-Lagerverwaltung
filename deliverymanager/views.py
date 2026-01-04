from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404, render, redirect

from ordermanager.models import Order
from deliveryitem.models import DeliveryItem
from .models import Delivery
from .serializers import DeliverySerializer


# -----------------------
# API (JSON)
# -----------------------
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
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = DeliverySerializer(delivery, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    delivery.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# -----------------------
# HTML PAGE (Create + List + Items in ONE page)
# -----------------------
def deliveries_page(request):
    # CREATE (via the form inside deliveries.html)
    if request.method == "POST":
        order_id = request.POST.get("order")
        delivery_date = request.POST.get("delivery_date")
        status_value = request.POST.get("status")
        delivered = True if status_value == "on" else False

        # Create Delivery
        delivery = Delivery.objects.create(
            order_id=order_id,
            delivery_date=delivery_date,
            status=delivered,
        )

        # Create up to 3 DeliveryItems (ignore empty rows)
        for i in range(1, 4):
            desc = (request.POST.get(f"description_{i}") or "").strip()
            qty_raw = (request.POST.get(f"quantity_{i}") or "").strip()

            if desc and qty_raw:
                try:
                    qty = int(qty_raw)
                except ValueError:
                    qty = 1

                if qty < 1:
                    qty = 1

                DeliveryItem.objects.create(
                    delivery=delivery,
                    description=desc,
                    quantity=qty,
                )

        return redirect("deliveries_page")

    # READ (render list + items)
    deliveries = Delivery.objects.prefetch_related("items").all()
    orders = Order.objects.all()

    return render(
        request,
        "deliverymanager/deliveries.html",
        {"deliveries": deliveries, "orders": orders},
    )