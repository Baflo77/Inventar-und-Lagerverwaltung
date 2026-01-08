from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from .models import Stock
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import StockSerializer


# Create your views here.
@api_view()
def show_stock(request):
    # 'select_related' optimiert die Datenbankabfrage für Fremdschlüssel (Product & Location)
    stocks = Stock.objects.select_related('product', 'location').all()

    context = {
        'stocks': stocks
    }
    return render(request, 'stockmanager/stockmanager.html', context)

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
    # 1. Daten holen (mit select_related für Performance)
    stocks = Stock.objects.select_related('product', 'location').all()

    context = {
        'stocks': stocks
    }

    # 2. An das Template schicken
    # WICHTIG: Prüfe, ob deine HTML-Datei wirklich in diesem Ordner liegt!
    return render(request, 'stockmanager/stockmanager.html', context)


# ... deine anderen Funktionen (outgoing_goods_view etc.) kannst du lassen ..


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OutgoingStockForm
from .services import process_outgoing_goods
from django.core.exceptions import ValidationError


def outgoing_goods_view(request):
    if request.method == 'POST':
        form = OutgoingStockForm(request.POST)
        if form.is_valid():
            stock_item = form.cleaned_data['stock_item']
            quantity = form.cleaned_data['quantity']
            notes = form.cleaned_data['notes']

            try:
                process_outgoing_goods(stock_item.id, quantity, user=request.user, notes=notes)
                messages.success(request, f"{quantity}x {stock_item.product} erfolgreich ausgebucht.")
                return redirect('stock_list_ui')  # Zurück zur Übersicht
            except ValidationError as e:
                # Fehler aus dem Service im Formular anzeigen
                form.add_error(None, e)
    else:
        form = OutgoingStockForm()

    return render(request, 'stockmanager/outgoing_form.html', {'form': form})