from django import forms
from stockmanager.models import Stock

class OutgoingStockForm(forms.Form):
    # Wir lassen den Nutzer direkt den Stock-Eintrag wählen (z.B. "iPhone 15 - Regal A")
    stock_item = forms.ModelChoiceField(
        queryset=Stock.objects.select_related('product', 'location').filter(quantity__gt=0),
        label="Lagerbestand wählen",
        empty_label="Bitte wählen..."
    )
    quantity = forms.IntegerField(min_value=1, label="Menge")
    notes = forms.CharField(required=False, widget=forms.Textarea, label="Notiz (optional)")