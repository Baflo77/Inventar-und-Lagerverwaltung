from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from rest_framework import status

from .models import Stock
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import StockSerializer


# Create your views here.
@api_view()
def show_stock(request):
    return Response("Hier sind deine Lager")

@api_view(["GET","POST"])
def show_all_stocks(request):
    if request.method == "GET":
        searchterm = request.query_params.get('searchterm')

        if searchterm is not None:
            stock= get_list_or_404(Stock, stock__icontains=searchterm)
        elif searchterm is not None:
            stock = Stock.objects.all()

        serialized_stock = StockSerializer(Stock, many=True)
        return Response(serialized_stock.data)
    elif request.method == "POST":
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(StockSerializer.data, status=status.HTTP_201_CREATED)
        return Response(StockSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET","PUT","DELETE"])
def show_stock_details(request, id):
    if request.method == "GET":
        stock = get_list_or_404(Stock)
        serialized_stock = StockSerializer(stock, many=True)
        return Response(serialized_stock.data)
    elif request.method == "DELETE":
        Stock.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == "PUT":
        serializer = StockSerializer(instance=Stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(StockSerializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def show_first_stock(request):
    stock = Stock.objects.first()
    return HttpResponse(f"Produkt: {stock.product}, Standort: {stock.location}, Anzahl: {stock.quantity}, Mindestbestand: {stock.threshold}, Status: {stock.status}, Warenhaus: {stock.warehouse}")

def write_stock(request):
    stock = Stock(product="Apple iPhone 15", location="Berlin", quantity=8, threshold=1, warehouse="W3")
    stock.save()
    stock = Stock.objects.last()
    return HttpResponse(f"Produkt: {stock.product}, Standort: {stock.location}, Anzahl: {stock.quantity}, Mindestbestand: {stock.threshold}, Status: {stock.status}, Warenhaus: {stock.warehouse}")


def stock_list_ui(request):
    searchterm = request.GET.get('searchterm')
    lagerbestandsdaten = Stock.objects.select_related('product', 'warehouse', 'location')
    if searchterm:
        suche_produkt = lagerbestandsdaten.filter(product__name__icontains=searchterm)
        suche_ort = lagerbestandsdaten.filter(location__name__icontains=searchterm)

        stocks = (suche_produkt | suche_ort).distinct()
    else:
        stocks = lagerbestandsdaten.all()

    stocks = stocks.order_by('product__name')

    context = {
        'stocks': stocks,
        'searchterm': searchterm
    }
    return render(request, 'stockmanager/stockmanager.html', context)