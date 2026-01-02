# stockmovementmanager/filters.py
import django_filters
from .models import StockMovement
from django import forms

class StockMovementFilter(django_filters.FilterSet):
    # 1. Datum von
    start_date = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='date__gte',
        label='Datum von',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # 2. Datum bis
    end_date = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='date__lte',
        label='Datum bis',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    # 3. Produkt (Suche nach Name)
    product = django_filters.CharFilter(
        field_name='product__name',
        lookup_expr='icontains',
        label='Produkt'
    )
    # 4. Typ (Auswahlfeld)
    movement_type = django_filters.ChoiceFilter(
        choices=StockMovement.MOVEMENT_TYPES,
        label='Typ'
    )

    class Meta:
        model = StockMovement
        # Die Felder hier leer lassen oder nur Metadaten,
        # da wir die Reihenfolge oben explizit definiert haben.
        fields = []