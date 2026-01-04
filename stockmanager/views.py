from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from .models import Stock
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import StockSerializer


# Create your views here.
@api_view()
def show_stock(request):
    return Response("Hier sind deine Lager")

@api_view()
def show_all_stocks_by_id(request, id):
    stock = get_list_or_404(Stock, pk=id)
    serializer = StockSerializer(stock, many=True)
    return Response(serializer.data)

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