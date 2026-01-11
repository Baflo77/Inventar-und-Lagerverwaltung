from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status as drf_status

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from ordermanager.models import Order
from deliveryitem.models import DeliveryItem
from .models import Delivery
from .serializers import DeliverySerializer
from django.db import transaction


# =========================
# API (JSON) - Swagger
# =========================

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
        return Response(serializer.data, status=drf_status.HTTP_201_CREATED)
    return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def show_delivery_details(request, pk):
    delivery = get_object_or_404(Delivery, pk=pk)

    if request.method == "GET":
        serializer = DeliverySerializer(delivery)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = DeliverySerializer(delivery, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=drf_status.HTTP_400_BAD_REQUEST)

    delivery.delete()
    return Response(status=drf_status.HTTP_204_NO_CONTENT)


# =========================
# HTML (Frontend) - DB CRUD
# =========================

def _normalize_delivery_status(raw: str) -> str:
    """Validiert + normalisiert Status-Wert."""
    value = (raw or Delivery.STATUS_OPEN).strip().lower()
    allowed = {Delivery.STATUS_OPEN, Delivery.STATUS_SHIPPED, Delivery.STATUS_DELIVERED}
    return value if value in allowed else Delivery.STATUS_OPEN


@login_required
def deliveries_page(request):
    """
    LIST + optional Create/Edit Mode (ähnlich wie customers_page):
    - /deliveries/?create=1  -> Formular anzeigen
    - /deliveries/?edit=ID   -> Edit-Formular anzeigen
    """
    create_mode = request.GET.get("create") == "1"
    edit_id = request.GET.get("edit")
    edit_delivery = None
    if edit_id:
        edit_delivery = get_object_or_404(Delivery, pk=edit_id)

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
        {
            "deliveries": deliveries,
            "orders": orders,
            "create_mode": create_mode,
            "edit_delivery": edit_delivery,
        },
    )


@login_required
def delivery_create(request):
    """Create läuft sauber in DB + optional Items (max 3) ODER OrderItems kopieren."""
    if request.method != "POST":
        return redirect("deliveries_page")

    order_id = (request.POST.get("order") or "").strip()
    delivery_date = (request.POST.get("delivery_date") or "").strip()
    status_value = _normalize_delivery_status(request.POST.get("status"))

    if not (order_id and delivery_date):
        messages.error(request, "Bitte Order und Lieferdatum ausfüllen.", extra_tags="deliveries")
        return redirect("deliveries_page")

    # ✅ NEU: Schalter aus dem Formular (Checkbox)
    from_orderitems = request.POST.get("from_orderitems") == "1"

    try:
        order_obj = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        messages.error(request, "Order wurde nicht gefunden.", extra_tags="deliveries")
        return redirect("deliveries_page")

    with transaction.atomic():
        if from_orderitems:
            # ✅ BEST: nutzt deine Methode im Order-Model (kopiert OrderItems -> DeliveryItems)
            delivery = order_obj.create_delivery_from_orderitems(
                delivery_date=delivery_date,
                status=status_value,
            )
        else:
            # ✅ wie bisher: manuelle Items (max 3)
            delivery = Delivery.objects.create(
                order_id=order_id,
                delivery_date=delivery_date,
                status=status_value,
            )

            for i in range(1, 4):
                desc = (request.POST.get(f"description_{i}") or "").strip()
                qty_raw = (request.POST.get(f"quantity_{i}") or "").strip()

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

    messages.success(request, "Lieferung wurde angelegt.", extra_tags="deliveries")
    return redirect("deliveries_page")


@login_required
def delivery_edit(request, id):
    """Edit läuft sauber in DB (hier nur Delivery-Felder)."""
    delivery = get_object_or_404(Delivery, pk=id)

    if request.method != "POST":
        return redirect(f"/deliveries/?edit={id}")

    order_id = (request.POST.get("order") or "").strip()
    delivery_date = (request.POST.get("delivery_date") or "").strip()
    status_value = _normalize_delivery_status(request.POST.get("status"))

    if not (order_id and delivery_date):
        messages.error(request, "Bitte Order und Lieferdatum ausfüllen.", extra_tags="deliveries")
        return redirect(f"/deliveries/?edit={id}")

    delivery.order_id = order_id
    delivery.delivery_date = delivery_date
    delivery.status = status_value
    delivery.save()

    # Items-Edit lassen wir bewusst stabil/simple weg (sonst wird’s komplexer).
    # Wenn du willst, bauen wir danach Items bearbeiten/löschen sauber dazu.

    messages.success(request, "Änderungen gespeichert.", extra_tags="deliveries")
    return redirect("deliveries_page")


@login_required
def delivery_status(request, id):
    """Status-Dropdown Update (POST) -> DB Update."""
    delivery = get_object_or_404(Delivery, pk=id)

    if request.method != "POST":
        return redirect("deliveries_page")

    delivery.status = _normalize_delivery_status(request.POST.get("status"))
    delivery.save()

    # kein extra message-spam bei jedem Dropdown-Klick
    return redirect("deliveries_page")


@login_required
def delivery_delete(request, id):
    """Delete nur Admin/Staff (serverseitig!)."""
    if not request.user.is_staff:
        return HttpResponseForbidden("Nur Administratoren dürfen Lieferungen löschen.")

    delivery = get_object_or_404(Delivery, pk=id)

    if request.method == "POST":
        delivery.delete()
        messages.success(request, "Lieferung gelöscht.", extra_tags="deliveries")
        return redirect("deliveries_page")

    return redirect("deliveries_page")