from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.core.exceptions import ValidationError
from stockmovementmanager.models import StockMovement
from stockmovementmanager.serializer import StockMovementSerializer
from stockmanager.services import process_outgoing_goods, process_stock_transfer


@api_view(["GET", "POST"])
def stock_movement_list(request):

    if request.method == "GET":
        product_id = request.query_params.get("product_id")
        movement_type = request.query_params.get("movement_type")
        movement = StockMovement.objects.all().order_by('-timestamp')

        if product_id is not None:
            movement = movement.filter(product_id=product_id)

        if movement_type is not None:
            movement = movement.filter(movement_type=movement_type)

        serializer = StockMovementSerializer(movement, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        typ = data.get('movement_type')

        try:
            if typ == 'OUT':
                if not data.get('stock_id'):
                    return Response(
                        {"error": "stock_id fehlt! Bitte angeben, von welchem Bestand gebucht wird."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                process_outgoing_goods(
                    stock_id=data.get('stock_id'),
                    quantity=int(data.get('quantity')),
                    notes=data.get('note')
                )
                return Response({"msg": "Warenausgang erfolgreich gebucht"}, status=status.HTTP_201_CREATED)

            elif typ == 'MOVE':
                if not data.get('source_stock_id') or not data.get('target_location_id'):
                    return Response(
                        {"error": "source_stock_id oder target_location_id fehlen"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                process_stock_transfer(
                    source_stock_id=data.get('source_stock_id'),
                    target_location_id=data.get('target_location_id'),
                    quantity=int(data.get('quantity')),
                    note = data.get('note')
                )
                return Response({"msg": "Umlagerung erfolgreich"}, status=status.HTTP_201_CREATED)

            # FALL 3: Standard (z.B. Wareneingang IN oder Korrekturen)
            else:
                serializer = StockMovementSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            # Fängt Logik-Fehler ab (z.B. "Nicht genug Bestand")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Fängt technische Fehler ab
            return Response({"error": f"Serverfehler: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET", "PUT", "DELETE"])
def stock_movement_detail(request, id):
    movement = get_object_or_404(StockMovement, id=id)

    if request.method == "GET":
        serializer = StockMovementSerializer(movement)
        return Response(serializer.data)

    elif request.method == "DELETE":
        movement.delete()
        return Response(data={"msg": "Bewegung gelöscht"}, status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = StockMovementSerializer(instance=movement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def stock_movement_ui(request):
    # 1. Alle Bewegungen holen (Neueste zuerst)
    movements = StockMovement.objects.all().order_by('-timestamp')

    # 2. Filter auslesen
    q = request.GET.get('q')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    move_type = request.GET.get('type')

    # 3. Filter anwenden
    if q:
        movements = movements.filter(product__name__icontains=q)
    if date_from:
        movements = movements.filter(timestamp__date__gte=date_from)
    if date_to:
        movements = movements.filter(timestamp__date__lte=date_to)
    if move_type:
        movements = movements.filter(movement_type=move_type)

    context = {
        'movements': movements
    }
    return render(request, 'stockmovementmanager/stockmovement.html', context)