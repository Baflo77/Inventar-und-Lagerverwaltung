from django.db import transaction
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import PurchaseOrder
from .serializers import PurchaseOrderSerializer
from locationmanager.models import Location
from purchaseorderitemmanager.models import PurchaseOrderItem
from stockmanager.models import Stock
from stockmovementmanager.models import StockMovement
from django.views.decorators.csrf import ensure_csrf_cookie


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
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
@permission_classes([IsAuthenticated])
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


@ensure_csrf_cookie
def purchaseorder_ui(request):
    orders = PurchaseOrder.objects.select_related("supplier").all().order_by("-created_at")
    return render(request, "purchaseordermanager/purchaseordermanager.html", {"orders": orders})

@ensure_csrf_cookie
def purchaseorder_receive_ui(request, id):
    order = get_object_or_404(PurchaseOrder.objects.select_related("supplier"), id=id)
    locations = Location.objects.select_related("warehouse").all()
    return render(
        request,
        "purchaseordermanager/purchaseorder_receive.html",
        {"order": order, "locations": locations,}
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def purchaseorder_receive_api(request, id):
    destination_location_id = request.data.get("destination_location_id")
    items = request.data.get("items", [])
    notes = (request.data.get("notes") or "").strip()  # aktuell nur akzeptiert

    if not destination_location_id:
        return Response({"error": "Ziel-Lagerort fehlt."}, status=status.HTTP_400_BAD_REQUEST)

    if not isinstance(items, list) or len(items) == 0:
        return Response({"error": "Keine Positionen übergeben."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            order = PurchaseOrder.objects.select_for_update().get(id=id)
            destination = Location.objects.get(id=int(destination_location_id))

            any_posted_qty = False

            for row in items:

                if not isinstance(row, dict):
                    return Response({"error": "Ungültiges Item-Format."}, status=status.HTTP_400_BAD_REQUEST)

                if "po_item_id" not in row:
                    return Response({"error": "po_item_id fehlt in items[]"}, status=status.HTTP_400_BAD_REQUEST)

                po_item_id = int(row.get("po_item_id"))
                qty = int(row.get("quantity", 0))

                if qty <= 0:
                    continue

                any_posted_qty = True

                poi = PurchaseOrderItem.objects.select_for_update().get(
                    id=po_item_id,
                    purchase_order=order
                )

                remaining = poi.quantity - poi.received_quantity
                if qty > remaining:
                    return Response(
                        {"error": f"Zu hohe Menge bei PO-Item #{poi.id}. Offen: {remaining}"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                stock, _ = Stock.objects.select_for_update().get_or_create(
                    product=poi.product,
                    location=destination,
                    defaults={"quantity": 0, "threshold": 0}
                )
                stock.quantity += qty

                if hasattr(stock, "quantity_on_order"):
                    stock.quantity_on_order = max(0, stock.quantity_on_order - qty)

                stock.save()

                StockMovement.objects.create(
                    product=poi.product,
                    source_location=None,
                    destination_location=destination,
                    quantity=qty,
                    movement_type="IN",
                )

                poi.received_quantity += qty
                poi.save()

            if not any_posted_qty:
                return Response(
                    {"error": "Bitte mindestens eine Menge > 0 eingeben."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            all_items = list(PurchaseOrderItem.objects.filter(purchase_order=order))
            if all_items and all(i.received_quantity >= i.quantity for i in all_items):
                order.status = "delivered"
                order.save()

        return Response({"success": True}, status=status.HTTP_200_OK)

    except PurchaseOrder.DoesNotExist:
        return Response({"error": "PurchaseOrder nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)
    except Location.DoesNotExist:
        return Response({"error": "Ziel-Lagerort nicht gefunden."}, status=status.HTTP_404_NOT_FOUND)
    except PurchaseOrderItem.DoesNotExist:
        return Response(
            {"error": "PurchaseOrderItem nicht gefunden oder gehört nicht zur Bestellung."},
            status=status.HTTP_404_NOT_FOUND
        )
    except (ValueError, TypeError):
        return Response({"error": "Ungültige Zahlenwerte übergeben."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


