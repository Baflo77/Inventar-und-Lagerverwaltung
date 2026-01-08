from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q  # Wichtig für die Suche

# Importiere dein Model und Serializer
from stockmovementmanager.models import StockMovement
from stockmovementmanager.serializer import StockMovementSerializer



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
        serializer = StockMovementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    # 1. Alle Bewegungen holen (Neueste zuerst durch Meta ordering im Model)
    movements = StockMovement.objects.all()

    # 2. Filter auslesen (passend zu den <input> Namen im HTML)
    q = request.GET.get('q')  # Suche
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    move_type = request.GET.get('type')  # Im HTML heißt das Feld name="type"

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