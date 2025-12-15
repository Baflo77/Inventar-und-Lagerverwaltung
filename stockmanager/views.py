from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from .models import Stock

# Create your views here.
def show_stock(request):
    return HttpResponse("Hier sind deine Lager")

def show_all_stocks_by_id(request, id):
    stock = get_list_or_404(Stock, pk=id)
    return HttpResponse(stock)

def show_first_stock(request):
    stock = Stock.objects.first()
    return HttpResponse(f"Produkt: {stock.product}, Standort: {stock.location}, Anzahl: {stock.quantity}, Mindestbestand: {stock.threshold}, Status: {stock.status}, Warenhaus: {stock.warehouse}")

def write_stock(request):
    stock = Stock(product="Apple iPhone 15", location="Berlin", quantity=8, threshold=1, warehouse="W3")
    stock.save()
    stock = Stock.objects.last()
    return HttpResponse(f"Produkt: {stock.product}, Standort: {stock.location}, Anzahl: {stock.quantity}, Mindestbestand: {stock.threshold}, Status: {stock.status}, Warenhaus: {stock.warehouse}")
