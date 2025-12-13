from django.shortcuts import render, get_list_or_404, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from stockmovementmanager.models import StockMovement
from stockmovementmanager.serializer import StockMovementSerializer
from rest_framework import status


# Create your views here.

@api_view(["GET" , "POST"])
def stock_movement_list(request):

    if request.method =="GET":
        #Nach was soll gefiltert werden?<---------------------------!!!!!!!!!!!!
        product_id = request.query_params.get("product_id")
        movement_type = request.query_params.get("movement_type")

        movement = StockMovement.objects.all()

        if product_id is not None:
            movement = movement.filter(product_id=product_id)

        if movement_type is not None:
            movement = movement.filter(movement_type=movement_type)

        serializer = StockMovementSerializer(movement, many=True)
        return Response (serializer.data)


    elif request.method =="Post":
        serializer = StockMovementSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def stock_movement_detail(request, id):

    movement = get_object_or_404 (StockMovement, id=id)

    #GET: Einzelnes Item anzeigen ---
    if request.method == "GET":
        serializer = StockMovementSerializer(movement)
        return Response(serializer.data)

    # DELETE: Item löschen
    elif request.method == "DELETE":
        movement.delete()
        return Response(
            data={"msg": "Bewegung gelöscht"},
            status=status.HTTP_204_NO_CONTENT
        )

    # --- PUT: Item updaten ---
    elif request.method == "PUT":
        serializer = StockMovementSerializer(instance=movement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

