from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from .models import Customer
from .serializers import CustomerSerializer


# -------------------------
# API (JSON) – bleibt (wie bei dir)
# -------------------------

@api_view(["GET"])
@permission_classes([AllowAny])
def show_customer(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def show_first_customer(request):
    customer = Customer.objects.first()
    if not customer:
        return Response({"detail": "No customers found."}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def show_customer_details(request, id):
    customer = get_object_or_404(Customer, id=id)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def write_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------
# HTML Page – Frontend (customers.html)
# -------------------------

def customers_page(request):
    customers = Customer.objects.all()

    # ✅ Edit-Mode via ?edit=<id>
    edit_customer = None
    edit_id = request.GET.get("edit")
    if edit_id:
        edit_customer = get_object_or_404(Customer, id=edit_id)

    # ✅ Create-Mode via ?create=1
    create_mode = bool(request.GET.get("create"))

    return render(request, "customermanager/customers.html", {
        "customers": customers,
        "edit_customer": edit_customer,
        "create_mode": create_mode,
    })


# -------------------------
# Helper: Felder aus POST ins Model schreiben (ohne forms.py)
# -------------------------

def _apply_post_to_customer(instance: Customer, post_data) -> None:
    """
    Überträgt POST-Felder automatisch auf das Customer-Model.
    Voraussetzung: <input name="..."> heißt genau wie das Model-Feld (z.B. name, email, zip, ...).
    """
    for field in instance._meta.fields:
        # PK nie überschreiben
        if field.primary_key:
            continue

        field_name = field.name

        # Checkbox/Boolean: kommt nur wenn "checked"
        if field.get_internal_type() == "BooleanField":
            setattr(instance, field_name, field_name in post_data)
            continue

        raw_value = post_data.get(field_name, None)

        # Wenn Input nicht im Formular ist: nicht überschreiben
        if raw_value is None:
            continue

        # Leerer String und null=True -> None speichern
        if raw_value == "" and getattr(field, "null", False):
            setattr(instance, field_name, None)
            continue

        # Typ-Konvertierung über Django Feldlogik
        try:
            setattr(instance, field_name, field.to_python(raw_value))
        except Exception:
            setattr(instance, field_name, raw_value)


# -------------------------
# HTML Actions – Create / Edit / Delete (ohne forms.py)
# -------------------------

def create_customer(request):
    if request.method == "POST":
        customer = Customer()
        _apply_post_to_customer(customer, request.POST)
        customer.save()
        messages.success(request, "Kunde wurde angelegt.")
        return redirect("customers_page")

    # Create nur per POST, GET -> zurück
    return redirect("customers_page")


def edit_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        _apply_post_to_customer(customer, request.POST)
        customer.save()
        messages.success(request, "Kunde wurde aktualisiert.")
        return redirect("customers_page")

    # GET auf /<id>/edit/ -> zurück auf Seite mit Edit-Modus
    return redirect(f"{redirect('customers_page').url}?edit={id}")


def delete_customer(request, id):
    customer = get_object_or_404(Customer, id=id)

    if request.method == "POST":
        customer.delete()
        messages.success(request, "Kunde wurde gelöscht.")
        return redirect("customers_page")

    # Delete nur per POST, GET -> zurück
    return redirect("customers_page")