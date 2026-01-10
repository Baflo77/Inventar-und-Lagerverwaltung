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
        # ✅ partial=True -> Updates sind flexibler (Swagger / API)
        serializer = DeliverySerializer(delivery, data=request.data, partial=True)
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

        # ✅ Neuer 3-stufiger Status (open/shipped/delivered)
        status_value = (request.POST.get("status") or Delivery.STATUS_OPEN).strip().lower()
        allowed = {Delivery.STATUS_OPEN, Delivery.STATUS_SHIPPED, Delivery.STATUS_DELIVERED}
        if status_value not in allowed:
            status_value = Delivery.STATUS_OPEN

        # Create Delivery
        delivery = Delivery.objects.create(
            order_id=order_id,
            delivery_date=delivery_date,
            status=status_value,
        )

        # Create up to 3 DeliveryItems (ignore empty rows)
        for i in range(1, 4):
            desc = (request.POST.get(f"description_{i}") or "").strip()
            qty_raw = (request.POST.get(f"quantity_{i}") or "").strip()

            # ✅ Wenn Beschreibung da ist, aber Menge leer -> default 1
            if not desc:
                continue

            try:
                qty = int(qty_raw) if qty_raw else 1
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
    deliveries = (
        Delivery.objects
        .select_related("order")
        .prefetch_related("items")
        .all()
        .order_by("-delivery_date", "-id")
    )
    orders = Order.objects.all().order_by("id")

    return render(
        request,
        "deliverymanager/deliveries.html",
        {"deliveries": deliveries, "orders": orders},
    )