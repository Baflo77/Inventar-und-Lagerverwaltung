from django.http import HttpResponse
from django.shortcuts import render, get_list_or_404
from rest_framework import status
from .models import Stock
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StockSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OutgoingStockForm
from .services import process_outgoing_goods
from django.core.exceptions import ValidationError



# Create your views here.
@api_view()
def show_stock(request):
    # 'select_related' optimiert die Datenbankabfrage für Fremdschlüssel (Product & Location)
    stocks = Stock.objects.select_related('product', 'location').all()

    context = {
        'stocks': stocks
    }
    return render(request, 'stockmanager/stockmanager.html', context)

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
    stock = get_list_or_404(Stock, id=id)

    if request.method == "GET":
        stock = get_list_or_404(Stock)
        serialized_stock = StockSerializer(stock)
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

'''Test Views- Können weg?
def show_first_stock(request):
    stock = Stock.objects.first()
    return HttpResponse(f"Produkt: {stock.product}, Standort: {stock.location}, Anzahl: {stock.quantity}, Mindestbestand: {stock.threshold}, Status: {stock.status}, Warenhaus: {stock.warehouse}")

def write_stock(request):
    stock = Stock(product="Apple iPhone 15", location="Berlin", quantity=8, threshold=1, warehouse="W3")
    stock.save()
    stock = Stock.objects.last()
    return HttpResponse(f"Produkt: {stock.product}, Standort: {stock.location}, Anzahl: {stock.quantity}, Mindestbestand: {stock.threshold}, Status: {stock.status}, Warenhaus: {stock.warehouse}")

'''

def stock_list_ui(request):

    stocks = Stock.objects.select_related('product', 'location').all()

    context = {
        'stocks': stocks
    }
    return render(request, 'stockmanager/stockmanager.html', context)



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